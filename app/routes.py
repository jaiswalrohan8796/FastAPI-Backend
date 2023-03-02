from fastapi import APIRouter, Request, Depends, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.utils import validate_signup_data, hash_password, check_password, make_new_user_dict, validate_login_data, create_access_token
from database.mongodb import insert_user, find_user_with_email, delete_todo_by_id, add_todo, find_todo_by_id, edit_todo_by_email_todo_id
from app.auth import get_current_user
import json

# app configurations
templates = Jinja2Templates(directory="templates")
api_router = APIRouter()


# ===================== Un-protected routes =========================

@api_router.get("/signup", tags=["signup"], response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "errors": []})


@api_router.get("/login", tags=["login"])
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})


@api_router.post("/signup")
async def handle_signup(request: Request):
    # extract form data
    signup_data = await request.form()
    # validate form data
    errors = validate_signup_data(signup_data)
    if len(errors) > 0:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": errors})
    # split fields
    username = signup_data["username"]
    email = signup_data["email"]
    password = signup_data["password"]
    # check if user already exists
    is_already_user = await find_user_with_email(email)
    if is_already_user is not None:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": ["Email already present. Login instead"]})
    # hash password
    password = hash_password(password)
    # make new user dict
    new_user = make_new_user_dict(username, email, password)
    # insert user into mongodb
    insert_ack = await insert_user(new_user)
    if insert_ack is False:
        return templates.TemplateResponse("signup.html", {"request": request, "errors": ["Internal Server Error"]})
    print(f"{username} named new user created !")
    return templates.TemplateResponse("login.html", {"request": request, "errors": []})


@api_router.post("/login")
async def handle_login(request: Request):
    form_data = await request.form()
    email = form_data["email"]
    password = form_data["password"]
    # validate login data
    errors = validate_login_data(form_data)
    if len(errors) > 0:
        return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
    user = await find_user_with_email(email)
    if user == None:
        return templates.TemplateResponse("login.html", {"request": request, "errors": ["User doesn't exist."]})
    is_password_matched = check_password(password, user["password"])
    if is_password_matched == False:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": ["Password incorrect."]})
    access_token = create_access_token(email)
    redirect_url = request.url_for("handle_app")
    redirect_response = RedirectResponse(
        url=redirect_url, status_code=status.HTTP_302_FOUND)
    redirect_response.set_cookie("token", access_token)
    return redirect_response

# ============== Protected Routes ==============


@api_router.post("/edit/{todo_id}")
async def handle_edit_save(request: Request, todo_id, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    user = user_data["user"]
    req_body = await request.body()
    new_todo = json.loads(req_body)
    res = await edit_todo_by_email_todo_id(user["email"], todo_id, new_todo["todo"])
    if res:
        return Response(content="Todo edited succesfully", status_code=status.HTTP_200_OK)
    else:
        return Response(content="Todo eduting failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_router.get("/edit/{todo_id}")
async def handle_edit(request: Request, todo_id, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    user = user_data["user"]
    todo = await find_todo_by_id(user["email"], todo_id)
    if todo is None:
        redirect_url = request.url_for("handle_app")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})


@api_router.post("/add")
async def handle_add(request: Request, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    user = user_data["user"]
    req_body = await request.body()
    req_body_dict = json.loads(req_body)
    todo_data = req_body_dict["todo"]
    add_res = await add_todo(user["email"], todo_data)
    if add_res:
        return Response(content="Todo added succesfully", status_code=status.HTTP_200_OK)
    else:
        return Response(content="Todo adding failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_router.delete("/delete/{todo_id}")
async def handle_delete(request: Request, todo_id, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        del_res = await delete_todo_by_id(user_data["user"]["email"], todo_id)
        if del_res:
            return Response(content=f"{todo_id} was deleted", status_code=status.HTTP_200_OK)
        else:
            return Response(content=f"{todo_id} deletion failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_router.get("/")
async def handle_app(request: Request, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    app_response = templates.TemplateResponse(
        "app.html", {"request": request, "user": user_data["user"]})
    return app_response


@api_router.get("/{path:path}")
async def handle_incorrect_route(request: Request, user_data=Depends(get_current_user)):
    if user_data is None:
        redirect_url = request.url_for("get_login")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        redirect_url = request.url_for("handle_app")
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

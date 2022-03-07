from datetime import datetime
from fastapi import FastAPI, Request, Cookie
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from starlette.middleware.sessions import SessionMiddleware 
from starlette.datastructures import URL, URLPath
import starlette.status as status
from starlette.responses import RedirectResponse,Response 
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app=FastAPI()
security = HTTPBasic()

app.mount("/static",StaticFiles(directory="static"),name="static")

app.add_middleware(SessionMiddleware, secret_key="MyApp")

templates=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def index(request : Request):
    return templates.TemplateResponse("index.html",{"request" : request})
URLPath(path="/")


@app.get("/register",response_class=HTMLResponse)
def register(request : Request):
    return templates.TemplateResponse("register.html",{"request" : request})
URLPath(path="/register")

@app.get("/login",response_class=HTMLResponse)
def login(request : Request):
    return templates.TemplateResponse("login.html",{"request" : request})
URLPath(path="/login")

@app.get("/ulogin",response_class=HTMLResponse)
def ulogin(request : Request):
    return templates.TemplateResponse("ulogin.html",{"request" : request})
URLPath(path="/ulogin")


@app.post("/ulogin", response_class=HTMLResponse)
def do_ulogin(request: Request, response: Response, emailid: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users where emailid=? and password=?", [emailid, password])
    users = cur.fetchone()
   
    if not users:
        return templates.TemplateResponse("ulogin.html", {"request": request, "msg": "Invalid Email-id or Password"})
   
    else:
        request.session.setdefault("uid", users['uid'])
        request.session.setdefault("isLogin", True)
        request.session.setdefault('emailid', emailid)
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/logout",response_class=HTMLResponse)
def logout(request : Request):
    request.session.clear()
    return RedirectResponse("/ulogin", status_code=status.HTTP_302_FOUND)
URLPath(path="/logout")

@app.get("/shop",response_class=HTMLResponse)
def shop(request : Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products")
    plants = cur.fetchall()
    con.close
    return templates.TemplateResponse("shop.html",{"request" : request})
URLPath(path="/shop")


@app.get("/mapping",response_class=HTMLResponse)
def mapping(request : Request):
    return templates.TemplateResponse("mapping.html",{"request" : request})
URLPath(path="/mapping")


@app.get("/uregister",response_class=HTMLResponse)
def uregister(request : Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory=sqlite3.Row
    cur = con.cursor()
    con.execute("select * from users")
    items = cur.fetchall
    con.close
    return templates.TemplateResponse("uregister.html",{"request" : request, "items": items})


@app.post("/uregister",response_class=HTMLResponse)
def addusers(request : Request, name : str =  Form(...), age : int = Form(...), gender : str = Form(...), phonenumber : str = Form(...), address:str =Form(...), emailid : str = Form(...), password:str = Form(...), vehicletype :str = Form(...), model :str = Form(...), myear:str = Form(...)  ):
    with sqlite3.connect("Mydb.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into users(name,age,gender,phonenumber,address,emailid,password,vehicletype,model,myear,role) values(?,?,?,?,?,?,?,?,?,?,?)",(name,age,gender,phonenumber,address,emailid,password,vehicletype,model,myear,"1"))
        con.commit()
    return RedirectResponse("/ulogin",status_code=status.HTTP_302_FOUND)
URLPath(path="/uregister")

@app.get("/spregister",response_class=HTMLResponse)
def spregister(request : Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory=sqlite3.Row
    cur = con.cursor()
    con.execute("select * from servicep")
    items = cur.fetchall
    con.close
    return templates.TemplateResponse("spregister.html",{"request" : request, "items": items})


@app.post("/spregister",response_class=HTMLResponse)
def addservicep(request : Request, name : str =  Form(...), age :  str = Form(...), phonenumber : str = Form(...), address:str =Form(...), emailid : str = Form(...), password : str = Form(...)  ):
    with sqlite3.connect("Mydb.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into servicep(name,age,phonenumber,address,emailid,password,role) values(?,?,?,?,?,?,?)",(name,age,phonenumber,address,emailid,password,"2"))
        con.commit()
    return RedirectResponse("/ulogin",status_code=status.HTTP_302_FOUND) 
URLPath(path="/spregister")

@app.get("/admin/", response_class=HTMLResponse)
def admin_index(request: Request):
    return templates.TemplateResponse("/admin/index.html", {"request": request})

@app.post("/admin/", response_class=HTMLResponse)
def admin_index(request: Request, username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from admin where username=? and password=?", [username, password])
    admin = cur.fetchone()
    if not admin:
        return templates.TemplateResponse("/admin/index.html", {"request": request, "msg": "Invalid usersname or Password"})
    else:
        request.session.setdefault("isLogin", True)
        request.session.setdefault('username', admin['username'])
        request.session.setdefault('uid', admin['id'])
        request.session.setdefault('role', admin['role'])
        return RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)
    
@app.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("/admin/dashboard.html", {"request": request })

@app.get("/admin/products", response_class=HTMLResponse)
def admin_products(request: Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products")
    products = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/products.html", {"request": request, "products": products})

@app.get("/admin/products/create", response_class=HTMLResponse)
def admin_products_create(request: Request):
    return templates.TemplateResponse("/admin/products_create.html", {"request": request})

@app.post("/admin/products/create", response_class=HTMLResponse)
def admin_products_create(request : Request, Pname:str = Form(...), Price: str = Form(...),  image: str = Form(...),category:str = Form(...)):
    with sqlite3.connect("Mydb.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into products(Pname, Price, image, category) values(?,?,?,? )",
                    (Pname, Price, image, category))
        con.commit()
    return RedirectResponse("/admin/products",status_code=status.HTTP_302_FOUND)

@app.get("/admin/logout",response_class=HTMLResponse)
def logout(request : Request):
    request.session.clear()
    return RedirectResponse("/admin/", status_code=status.HTTP_302_FOUND)
URLPath(path="/logout")




@app.get("/orders",response_class=HTMLResponse)
def orders(request : Request):
    if not request.session.get('isLogin'):
        return RedirectResponse('/ulogin', status_code=status.HTTP_302_FOUND)

    uid = request.session.get('uid')
    print(uid)

    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *,o.id as oid from users u, orders o, products p where u.uid=o.uid and o.pid=p.pid and o.uid =?",
                [uid])
    orders = cur.fetchall()
    con.close
    return templates.TemplateResponse("/order.html", {"request": request, "orders": orders})

@app.get("/admin/orders", response_class=HTMLResponse)
def admin_orders(request: Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *, o.id as oid from users u, products p, orders o where o.uid = u.uid and o.pid = p.pid")
    orders = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/orders.html", {"request": request, "orders": orders})

@app.get("/product", response_class=HTMLResponse)
def products(request: Request):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products")
    products = cur.fetchall()
    con.close
    print(products)
    return templates.TemplateResponse("/product.html", {"request" : request, "products": products })  


@app.get("/view/{pid}", response_class=HTMLResponse)
def view(request: Request, pid: int = 0): 
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where pid =?", [pid])
    product = cur.fetchall()
    con.close
    return templates.TemplateResponse("/view.html", {"request": request, "product": product[0]}) 


@app.get("/delete/{pid}", response_class=HTMLResponse)
def view(request: Request, pid: int = 0): 
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("delete from products where pid =?", [pid])
    con.commit()
    con.close
    return RedirectResponse("/admin/products", status_code=status.HTTP_302_FOUND) 

@app.get("/admin/orders_view/{oid}", response_class=HTMLResponse)
def admin_order_view(request: Request, oid: int = 0):
    return templates.TemplateResponse("/admin/orders_view.html", {"request": request})

@app.get("/details/{pid}", response_class=HTMLResponse)
def details(request: Request, pid: int):
    if not request.session.get('isLogin'):
        return RedirectResponse('/ulogin', status_code=status.HTTP_302_FOUND)

    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where pid =?", [pid])
    description = cur.fetchall()
    con.close

    return templates.TemplateResponse("details.html", {"request": request, "pid": pid, "description": description[0]})


@app.get("/addtocart", response_class=HTMLResponse)
async def addtocart(request: Request, pid:int = 1, qty:int = 1):
    uid = request.session.get('uid')
    with sqlite3.connect("Mydb.db", check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute("INSERT into cart(pid, qty, uid) values(?,?,?)",
                    (pid, qty, uid))
        con.commit()
    return RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)


@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    if not request.session.get('isLogin'):
        return RedirectResponse('/ulogin', status_code=status.HTTP_302_FOUND)

    uid = request.session.get('uid')

    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *,c.uid as cid from users u,cart c, products p where u.uid=c.uid and c.pid=p.pid and c.uid =?", [uid])
    items = cur.fetchall()
    con.close
    total = sum(map(lambda item: int(item['qty']) * int(item['price']), items ))
    return templates.TemplateResponse("/cart.html", {"request": request, "total": total,  "items": items})


@app.get("/confrim", response_class=HTMLResponse)
def confrim(request: Request):
    uid = request.session.get('uid')
    with sqlite3.connect("Mydb.db", check_same_thread=False) as con:
        cur = con.cursor()

        cur.execute("SELECT * from cart where uid = ? ",[uid])
        carts = cur.fetchall()
        for cart in carts:
            print(cart)
            now = datetime.now()
            order_time = now.strftime("%d/%m/%Y %H:%M:%S")
            cur.execute("INSERT into orders(pid, qty, uid,status,date) values(?,?,?,?,?)",
                        [cart[1], cart[2], cart[3], "ORDERED", order_time])
        cur.execute("Delete from cart where uid = ? ", [uid])
        con.commit()

    return RedirectResponse("/orders", status_code=status.HTTP_302_FOUND)


@app.get("/deletecart/{cid}", response_class=HTMLResponse)
def delete_cart_item(request: Request, cid: int):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("Delete from cart where id =?", [cid])
    con.commit()
    con.close
    return RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)

@app.get("/splogin",response_class=HTMLResponse)
def login(request : Request):
    return templates.TemplateResponse("splogin.html",{"request" : request})
URLPath(path="/splogin")

@app.post("/splogin", response_class=HTMLResponse)
def do_login(request: Request, response: Response, emailid: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("Mydb.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from servicep where emailid=? and password=?", [emailid, password])
    users = cur.fetchone()

    @app.post("/splogin", response_class=HTMLResponse)
    def do_splogin(request: Request, response: Response, emailid: str = Form(...), password: str = Form(...)):
     con = sqlite3.connect("Mydb.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from servicep where emailid=? and password=?", [emailid, password])
     users = cur.fetchone()
   
    if not users:
        return templates.TemplateResponse("splogin.html", {"request": request, "msg": "Invalid Email-id or Password"})
   
    else:
        request.session.setdefault("uid", users['spid'])
        request.session.setdefault("isLogin", True)
        request.session.setdefault('emailid', emailid)
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get("/about",response_class=HTMLResponse)
def about(request : Request):
    return templates.TemplateResponse("about.html",{"request" : request})
URLPath(path="/about")
from flask import Flask,render_template,request,flash
from data import salary_list
app = Flask(__name__)
@app.route('/')
def hello():
    #返回网页模板
    return render_template('index.html')

@app.route('/login',methods=["post"])
def login():
    #登录到服务器，获取用户名和密码，然后进行校验，记录信息，在返回后台页面
    """request.form.get("username")
    request.form.get("password")
    print("登录成功")"""

    username=request.form.get("username")
    password=request.form.get("password")

    # 登录校验
    found = False  # 添加一个标志变量来跟踪是否找到匹配项
    #管理员登录
    for salary in salary_list:
        if username == salary["username"] and password == salary["password"] and 2== salary["level"]:
            print("登录成功")
            return render_template('admin.html', salary_list=salary_list)
            found = True  # 标记找到匹配项
            break  # 找到匹配项后退出循环
    #普通用户登录
        elif username == salary["username"] and password == salary["password"] and 1== salary["level"]:
            print("登录成功")
            return render_template('user.html', salary_list=salary_list)
            found = True
            break

    if not found:  # 检查是否找到匹配项
        print("登录失败")
        return render_template('index.html')


# 删除用户
@app.route('/delete/<name>')
def delete(name):
    #删除用户
    for salary in salary_list:
        if salary["username"] == name:
            salary_list.remove(salary)
            print("删除成功")
            return render_template('admin.html', salary_list=salary_list)
# 修改用户
@app.route('/change/<name>')
def update(name):
    #修改用户
    for salary in salary_list:
        if salary["username"] == name:
            return render_template('change.html', user=salary)
    return  render_template('admin.html', salary_list=salary_list)

@app.route('/changed/<name>' , methods=["post"])
def changed(name):
    #拿到提交的修改信息
    for salary in salary_list:
        if salary["username"] == name:
            salary['username']=request.form.get('username')
            salary['salary'] = request.form.get('salary')
            salary['department'] = request.form.get('department')
            salary['position'] = request.form.get('position')
            salary['password'] = request.form.get('password')
            salary['level'] = request.form.get('level')
    return render_template('admin.html', salary_list=salary_list)
# 增加用户
@app.route('/add',methods=["GET","POST"])
def add():
    if request.method=="GET":
        return render_template('add.html')
    if request.method== "POST":
        username = request.form.get("username")
        salary = request.form.get("salary")
        department = request.form.get("department")
        position = request.form.get("position")
        password=request.form.get("password")
        level=request.form.get("level")
        salary_list.append({"username":username,"salary":salary, "department":department, "position":position,"password":password,"level":level,})
    return render_template('admin.html', salary_list=salary_list)


if __name__ == "__main__":
    app.run()

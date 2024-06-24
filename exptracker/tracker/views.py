from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# Create your views here.

def home(request):
    #return render(request, 'auth-signin.html')
    return render(request, 'dashboard.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def activity_add(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    if request.method == "POST":
        ac_name = request.POST.get('txtActName')
        ac_desc = request.POST.get('txtAcDesc')
        expense = float( request.POST.get('txtExpense'))
        a_cat = request.POST.get('ddlCat')
        a_date = request.POST.get('txtActDate')
        payload = {
            'ac_name': ac_name,
            'ac_desc': ac_desc,
            'expense': expense,
            'a_cat': a_cat,
            'a_date': a_date
        }
        print(payload)
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Activity added successfully with ID: {data['ac_id']}")
            else:
                messages.warning(request, "Failed to add activity.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")
        return redirect('add-activity')

    # Fetch categories for the dropdown
    try:
        categories_url = 'http://localhost:8085/finapi/category/'
        categories_response = requests.get(categories_url)
        if categories_response.status_code == 200:
            categories = categories_response.json()
        else:
            categories = []
            messages.warning(request, "Failed to retrieve categories.")
    except Exception as ex:
        print(ex)
        categories = []
        messages.warning(request, "An error occurred while fetching categories.")

    return render(request, 'activity-add.html', {'categories': categories})



# ------------ get list of activities -------------------
def getactdata(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return render(request, 'activities.html', {'acdata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return render(request, 'index.html')

#---------------------EDit Activities----------------------

def edit_activity(request, ac_id):
    url = f'http://localhost:8085/finapi/activity/{ac_id}/'
    categories_url = 'http://localhost:8085/finapi/category/'

    if request.method == "POST":
        ac_name = request.POST.get('txtActName')
        ac_desc = request.POST.get('txtAcDesc')
        expense = request.POST.get('txtExpense')
        a_cat = request.POST.get('ddlCat')
        a_date = request.POST.get('txtActDate')

        payload = {
            'ac_name': ac_name,
            'ac_desc': ac_desc,
            'expense': expense,
            'a_cat': a_cat,
            'a_date': a_date
        }
        try:
            response = requests.put(url, json=payload)
            if response.status_code == 200:
                messages.success(request, "Activity updated successfully.")
                return redirect('get-act')
            else:
                messages.warning(request, "Failed to update activity.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the update process.")

    try:
        activity_response = requests.get(url)
        categories_response = requests.get(categories_url)
        if activity_response.status_code == 200 and categories_response.status_code == 200:
            activity_data = activity_response.json()
            categories = categories_response.json()
            return render(request, 'activity_edit.html', {'activity_data': activity_data, 'categories': categories})
        else:
            messages.warning(request, "Failed to retrieve activity or categories.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")

    return redirect('get-act')

# def edit_activity(request, ac_id):
#     url = f'http://localhost:8085/finapi/activity/{ac_id}'  # must terminate with /
    

#     if request.method == "POST":
#         ac_name = request.POST.get('txtActName')
#         ac_desc = request.POST.get('txtAcDesc')
#         expense = request.POST.get('txtExpense')
#         a_cat = request.POST.get('ddlCat')
#         a_date = request.POST.get('txtActDate')

#         payload = {
#             'ac_name': ac_name,
#             'ac_desc': ac_desc,
#             'expense': expense,
#             'a_cat': a_cat,
#             'a_date': a_date
#         }

#         response = requests.put(url, json=payload)

#         if response.status_code == 200:   # response 200
#             data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
#             #messages.success(request, f"Details updated successfully with Name: {data['ac_name']}, Expense: {data['expense']}, Description: {data['ac_desc']}, Category: {data['a_cat']}, Date: {data['a_date']}")
#         else:
#             messages.warning(request, "Some error occurred during update, check logs for details")

#         return redirect('/trackmyexp/getact')  # redirect to view all

#     else:  # * * * * * * * get details of the selected activity by API Call  * * * * * * * 
#         response = requests.get(url)
#         if response.status_code==200:
#             data=response.json()
#             return render(request, 'activity_edit.html',{'acdata':data})




#------------------------DELTE Activity ------------------------
def del_activity(request, ac_id):
    url = f'http://127.0.0.1:8085/finapi/activity/{ac_id}/'

    try:
        response = requests.delete(url)
    
        if response.status_code == 204:
            messages.success(request, "Activity deleted successfully.")
        else:
            messages.warning(request, "Failed to delete activity. Remote server did not respond properly.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred during the delete process. Check logs for details.")

    return redirect('get-act')





def save_cat(request):
    url = 'http://localhost:8085/finapi/category/'
    if request.method == "POST":
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')

        payload = {
            'cat_name': cname, 
            'budget': bplan
            }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Details stored successfully with ID: {data['cat_id']} and Name: {data['cat_name']}")
            else:
                messages.warning(request, "Failed to save data.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")
    return render(request, 'category_add.html')

def get_catlist(request):
    url = 'http://localhost:8085/finapi/category/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return render(request, 'category.html', {'categorydata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return render(request, 'dashboard.html') #***********

def edit_cat(request, cat_id):
    url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'  # must teminate with /

    if request.method == "POST":
        
        # get data from form
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')
        
        # cstatus = request.POST.get('rating') checkbox handling later
       

        payload = {
            'cat_name': cname,
            'budget': bplan
            
        }

        response = requests.put(url, json = payload)  # send as JSON

        if response.status_code == 200:   # response 200
            data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
            print(data)
            # return data
            messages.success(request, "Details updated successfully with Name: " + str(data["cat_name"]) + ", Budget: " + str(data["budget"]))
            
        else:
            messages.warning(request, "Some error occured during update, check logs for details")
            #return None

        return redirect('/trackmyexp/getcategorylist')  # redirect to view all

    else:  # * * * * * * * get details of the selected company by API Call  * * * * * * * 

        response = requests.get(url) #.json()
        if response.status_code == 200:
            data = response.json()
            return render(request, 'category_edit.html', {'categorydata' : data})
        

        # --------------- DELETE (One)----------------------
def del_cat(request, cat_id):
    url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'

    try:
        response = requests.delete(url)
    
        if response.status_code == 204:
            messages.success(request, "Details deleted successfully")
        else:
            messages.warning(request, "Failed to delete resource..remote server did not respond properly")
    except Exception as ex:
        print(ex)
        messages.warning(request, "Some error occured during delete, check logs for details")

    return redirect('/trackmyexp/getcategorylist')


def userlogin(request):
    url = 'http://localhost:8088/api/login/'
    if request.method == "POST":
        uname = request.POST.get('txtUname')
        upass = request.POST.get('txtPassword')

        payload = {
            'username': uname, 
            'password': upass
            }
        
        print(payload)

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                messages.success(request, f"Login successfull with token id: {data['token']}")
                return redirect('/trackmyexp/dash')
            else:
                messages.warning(request, "Login failed.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during remote authentication.")
    return render(request, 'auth-signin.html')

def userregister(request):
    url = 'http://localhost:8088/api/register/'
    if request.method == "POST":
        uname = request.POST.get('txtUname')
        email=request.POST.get('txtEmail')
        upass = request.POST.get('txtPassword')

        payload = {
            'username': uname,
            'email':email, 
            'password': upass
            }
        
        print(payload)

        try:
            response = requests.post(url, json=payload)
            print(response.status_code)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Registered successfull ")
                return redirect('/trackmyexp/userlogin')
            else:
                messages.warning(request, "Registration failed.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during remote authentication.")
    return render(request, 'auth-signup.html')



def userlogin(request):
    url = 'http://localhost:8088/api/login/'
    if request.method == "POST":
        uname = request.POST.get('txtUname')
        upass = request.POST.get('txtPassword')

        payload = {
            'username': uname, 
            'password': upass
            }
        
        print(payload)

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                messages.success(request, f"Login successfull with token id: {data['token']}")
                return redirect('/trackmyexp/dash')
            else:
                messages.warning(request, "Login failed.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during remote authentication.")
    return render(request, 'auth-signin.html')





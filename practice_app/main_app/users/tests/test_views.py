from http import client
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import UserProfile

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self._user = User.objects.create(
            username='username_try',
            password='password_try_10',
            email='username_try@gmail.com'
        )

        self.test_data = {
            'username': 'test_name',
            'email': 'email@gmail.com',
            'password': 'Password10'
        }
        self.test_data_wrong_email = {
            'username': 'test_name',
            'email': 'a',
            'password': 'Password'
        }

        self.api_user_url = 'http://127.0.0.1:8000/api/users/'
        self.getUsers_url = reverse('all-users')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_getUsers_GET(self):
        response = self.client.get(self.getUsers_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/ListAllUsers.html')

    def test_create_user_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_api_create_user_POST(self):
        response = self.client.post(self.api_user_url, self.test_data)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['email'], 'email@gmail.com')
        self.assertEquals(response.data['username'], 'test_name')

    def test_api_create_user_not_unique_email(self):
        response = self.client.post(self.api_user_url, self.test_data_wrong_email)
        self.assertEquals(response.status_code, 400)

    def test_api_create_user_wrong_email(self):
        response = self.client.post(self.api_user_url, self.test_data_wrong_email)
        self.assertEquals(response.status_code, 400)

    def test_api_create_user_existing_email(self):
        response = self.client.post(self.api_user_url, self.test_data)
        response_ = self.client.post(self.api_user_url, self.test_data)
        self.assertEquals(response_.status_code, 400)

        
        
class ProfileEditView(UpdateView):
    model= UserProfile
    fields = ['name', 'surname', 'city', 'country', 'bio']
    template_name = 'users/profile_edit.html'


    def get_object(self):
        
        return get_object_or_404(UserProfile, user__username=self.request.user.username)

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@api_view(["GET"])
def get_all_profiles(request):
    profiles = UserProfile.objects.all()
    profiles_dict = {
        userProfile.user.username: {
            "name": userProfile.name,
            "surname": userProfile.surname, 
            "city":userProfile.city,
            "country":userProfile.country,
            "bio": userProfile.bio,
            "email": userProfile.user.email}
      for userProfile in profiles}    
    response_json = json.dumps(profiles_dict)
    return HttpResponse(response_json, content_type="text/json")

@api_view(["POST"])
def edit_profile(request):
    body_unicode = request.body.decode('utf-8')
    body:dict = json.loads(body_unicode)
    username = body.get("username")
    if username == None:
        return HttpResponse("<h1>'{}' is not a valid username.</h1>".format(username))
    profile = get_object_or_404(UserProfile, user__username=username)
    changed_list = []
    unvalid_list = []
    bool_null = False
    del body["username"]
    for name, values in body.items():
        if name in ["name","surname","city","country","bio"]:
            if values == None:
                bool_null = True
                continue
            setattr(profile,name,values)
            changed_list.append(name)
        else:
            unvalid_list.append(name)
            
    profile.save()
    
    warning_text = ""
    if bool_null:
        warning_text = "<h1>Warning: Fields can not be null!</h1> "
    if unvalid_list:
        warning_text += "<h1>Warning: {} are not valid profile fields!</h1> ".format(', '.join(map(str, unvalid_list)))
    if not changed_list:
        return HttpResponse(warning_text + "<h1> Any fields didn't change on '{}' profile. </h1>".format(username))
    return HttpResponse(warning_text + "<h1>{} has changed on '{}' profile. </h1>".format(', '.join(map(str, changed_list)), username))    


@api_view(['GET'])
def getJoke(request):
    """
    Random joke generator.
    """
    api_response=requests.get("https://v2.jokeapi.dev/joke/Any?type=twopart")
    api_response = api_response.json()
    if api_response["error"] == False:
        joke = {
            'setup' : api_response["setup"],
            'delivery' : api_response["delivery"]
        }
        return render(
            request, 'post/display_jokes.html',{'joke' : joke}
        )
    else: 
        return render({
            'status' : 'non-existent'
        },status = 404) 

@api_view(['GET'])
def get_new_face(request):
    try:
        response=requests.get("https://randomuser.me/api/")
        json_response = response.json()
    except requests.exceptions.RequestException as error:
        messages.warning(request, 'A error occured while creating your new face, please try again later.')
        return redirect('home-page') 
    pic_url = json_response["results"][0]["picture"]["large"]
        
    return render(request, 'post/new_face.html',{'pic' : pic_url}) 

        


class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.initAlexaData = {"name" : "alexa", "surname": "alexasurname", "city" : "alexacity", "country": "alexacountry", "bio": "alexabio"}
        self.initCatilData = {"name" : "catil", "surname": "catilsurname", "city" : "catilcity", "country": "catilcountry", "bio": "catilbio"}
        self.modifiedAlexaData = {"username": "alexa","name" : "alexa2", "surname": "alexasurname2", "city" : "alexacity2", "country": "alexacountry2", "bio": "alexabio2"}
        self.alexa = User.objects.create(username="alexa", password="mypassword33A", email='alexa@gmail.com')
        self.catil = User.objects.create(username="catil", password="mypassword34B", email='alexa@gmail.com')
        self.alexaProfile = get_object_or_404(UserProfile, user__username="alexa")
        self.catilProfile = get_object_or_404(UserProfile, user__username="catil")

        for attr, value in self.initAlexaData.items(): 
            setattr(self.alexaProfile, attr, value)
        self.alexaProfile.save()

        for attr, value in self.initCatilData.items(): 
            setattr(self.catilProfile, attr, value)
        self.catilProfile.save()

    def get_profile_info_work(self):
        """People can fetch profile infos of all users with api"""
        json_response = self.client.get(reverse("all-profile-api"))
        dict_response = json_response.json
        alexa_dict = dict_response["alexa"]
        catil_dict = dict_response["catil"]
        for k in self.initAlexaData.keys():
            self.assertEqual(alexa_dict[k], self.initAlexaData[k])
        for k in self.initCatilData.keys():
            self.assertEqual(catil_dict[k], self.initCatilData[k])


    def change_profile_info_work(self):
        """People can change profile infos of selected user with api"""
        self.client.post(reverse("profile-edit-api"), data=self.modifiedAlexaData)
        self.assertEqual(self.alexaProfile.name, self.modifiedAlexaData["name"])
        self.assertEqual(self.alexaProfile.surname, self.modifiedAlexaData["surname"])
        self.assertEqual(self.alexaProfile.city, self.modifiedAlexaData["city"])
        self.assertEqual(self.alexaProfile.country, self.modifiedAlexaData["country"])
        self.assertEqual(self.alexaProfile.bio, self.modifiedAlexaData["bio"])
        """ This Api give info about username not found
                                     if data has some wrong fields, it list them and change true fields
                                     also it inform user about updated fields
                                     as html file.
            If I only return response status of the api, I could write more test cases but it cause a info loss
            So I preffered the more informative api. """


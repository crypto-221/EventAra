from flask import Flask , render_template , request , session , redirect , url_for
import pymysql as sql
from datetime import datetime, timezone
import geocoder
app = Flask(__name__)
app.secret_key = "EVENTARA"


@app.route("/")
def home():
    user = session.get("user" , None)
    if user:
        return render_template("searchEvent.html")
    return render_template("eventfinder.html")


@app.route("/aftersignup" , methods = ['POST'])
def sign():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            conn = sql.connect(user ="root" , password = "" , port = 3306 , database = "Event")
            cur = conn.cursor()
        except Exception as e :
            return render_template("eventfinder.html" ,  error="Database server is not running. Please start XAMPP/MySQL.")
        else:
            check = f"select * from signup where email = '{email}'"
            ch = cur.execute(check)
            if ch :
                return render_template("eventfinder.html" , err =  "Email already exists....")

            else:
                query = f"insert into signup values ('{email}' , '{password}' , '{name}')"
                cur.execute(query)
                conn.commit()
                conn.close()
    return render_template("eventfinder.html")


@app.route("/afterlogin" , methods = ['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        user = email.split('@')
        user = user[0]
        password = request.form.get("password")
        try:
            conn = sql.connect(user = 'root' , password = '' , port = 3306 , database = 'Event')
            cur = conn.cursor()
            query = f"select * from signup where email = '{email}' and password = '{password}'"
            data = cur.execute(query)

        except Exception as e :
            return render_template("eventfinder.html",error="Database server is not running. Please start XAMPP/MySQL."
            )

        if data:
            session['user'] = user
            return render_template("searchEvent.html" , user = user)

        else:
            return render_template("eventfinder.html", error = "invalid email or password")

@app.route("/logout")
def logout():
    session.popitem()
    return redirect(url_for(("home")))

@app.route("/about")
def about():
    return render_template("about.html")

API_KEY = "l0okN6X3PB3bTVwkRZNI0uw5zDMhTX-z7lg2YME1"
cities = {
    "jaipur":     (26.9124, 75.7873),
    "delhi":      (28.6139, 77.2090),
    "mumbai":     (19.0760, 72.8777),
    "bangalore":  (12.9716, 77.5946),
    "pune":       (18.5204, 73.8567),
    "hyderabad":  (17.3850, 78.4867),
    "kolkata":    (22.5726, 88.3639),
    "chennai":    (13.0827, 80.2707),
    "lucknow":    (26.8467, 80.9462),
    "chandigarh": (30.7333, 76.7794),
    "ahmedabad":  (23.0225, 72.5714),
    "surat":      (21.1702, 72.8311),
    "goa":        (15.2993, 74.1240),
    "kochi":      (9.9312,  76.2673),
    "coimbatore": (11.0168, 76.9558),
    "agra":       (27.1767, 78.0081),
    "varanasi":   (25.3176, 82.9739),
    "bhubaneswar":(20.2961, 85.8245),
    "patna":      (25.5941, 85.1376),
    "guwahati":   (26.1445, 91.7362),
}
@app.route("/event", methods=["POST"])
def city():
    import requests
    city_name = request.form.get("city").lower()
    if city_name not in cities:
        return "City not found"

    lat, lon = cities[city_name]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = "https://api.predicthq.com/v1/events/"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "country": "IN",
        "limit": 15,
        "location_around.origin": f"{lat},{lon}",
        "location_around.radius": "50km",
        "start.gte": today,
        "state": "active"
    }
    try :
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401:
            return render_template("searchEvent.html",error="Invalid API key. Please check API configuration.")
        elif response.status_code == 429:
            return render_template("searchEvent.html",error="API request limit exceeded. Please try again later.")

        elif response.status_code != 200:
            return render_template(
            "searchEvent.html",
            error="Unable to fetch events at the moment."
        )
        data = response.json()

    except Exception as e:
        return render_template(
        "searchEvent.html",
        error="Something went wrong while fetching events."
    )
    events_list = []
    for i in data['results']:
        start = i.get("start_local")
        category = i.get("category")
        address = i.get('geo', {}).get('address', {}).get('formatted_address', 'Location Not Available')
        events_list.append({
            "title": i.get("title"),
            "date": start.split("T")[0] if start else None,
            "category" : category ,
            "address" : address
        })
        print(address)
    # print(events_list)
    return render_template("new.html", events=events_list, city=city_name)



@app.route("/location"  , methods = ['POST' , 'GET'])
def location():
    data = geocoder.ip('me')
    city = data.city
    city = city.lower()
    # print(city)
    import requests
    if city not in cities:
        return "City not found"

    lat, lon = cities[city]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = "https://api.predicthq.com/v1/events/"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "country": "IN",
        "limit": 15,
        "location_around.origin": f"{lat},{lon}",
        "location_around.radius": "50km",
        "start.gte": today,
        "state": "active"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    events_list = []
    for i in data['results']:
        start = i.get("start_local")
        category = i.get("category")
        address = i.get('geo', {}).get('address', {}).get('formatted_address', 'Location Not Available')
        events_list.append({
            "title": i.get("title"),
            "date": start.split("T")[0] if start else None,
            "category" : category ,
            "address" : address
        })
    # print(events_list)
    # return render_template("new.html", events=events_list, city=city)
    return  redirect(url_for("new.html", events=events_list, city=city))




@app.route("/searchEvent")
def search():
    return render_template('search.html')


@app.route("/afterlogin")
def search_event():
    return render_template("searchEvent.html")
app.run(debug = True , port = 5000)






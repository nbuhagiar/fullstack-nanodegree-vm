#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output += "<html><body>"
                output += "<a href='/restaurants/new'> Make a New Restaurant Here </a></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants"
                    output += "/%s/edit'> Edit </a>" % restaurant.restaurant_id
                    output += "</br>"
                    output += "<a href='/restaurants"
                    output += "/%s/delete'> Delete </a>" % restaurant.restaurant_id
                    output += "</br></br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Make a New Restaurant </h1>"
                output += "<form method='POST' "
                output += "enctype='multipart/form-data' "
                output += "action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):                
                restaurant_id = self.path.split("/")[2]
                restaurant = (session.query(Restaurant)
                                     .filter_by(restaurant_id=restaurant_id)
                                     .one())
                if restaurant != []:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += restaurant.name
                    output += "</h1>"
                    output += "<form method='POST' "
                    output += "enctype='multipart/form-data' "
                    output += "action='/restaurants/"
                    output += "%s/edit'>" % restaurant.restaurant_id
                    output += "<input name='newRestaurantName'"
                    output += " type='text' "
                    output += "placeholder='%s'>" % restaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
            if self.path.endswith("/delete"):                
                restaurant_id = self.path.split("/")[2]
                restaurant = (session.query(Restaurant)
                                     .filter_by(restaurant_id=restaurant_id)
                                     .one())
                if restaurant != []:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure"
                    output += " you want to delete %s?" % restaurant.name
                    output += "</h1>"
                    output += "<form method='POST' "
                    output += "enctype='multipart/form-data' "
                    output += "action='/restaurants/"
                    output += "%s/delete'>" % restaurant.restaurant_id
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return    
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get("newRestaurantName")
                restaurant_id = self.path.split("/")[2]
                restaurant = (session.query(Restaurant)
                                     .filter_by(restaurant_id=restaurant_id)
                                     .one())
                if restaurant != []:
                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/restaurants")
                    self.end_headers()
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get("newRestaurantName")
                restaurant_id = self.path.split("/")[2]
                restaurant = (session.query(Restaurant)
                                     .filter_by(restaurant_id=restaurant_id)
                                     .one())
                if restaurant != []:
                    session.delete(restaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/restaurants")
                    self.end_headers()
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get("newRestaurantName")
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                return
        except:
            pass

def main():

    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == "__main__":
    main()

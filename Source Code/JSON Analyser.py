#import relevant plugins and libraries 
import tkinter as tk #imported for use of the gui
import json #to handle json files
import folium #to ploy data to maps
from tkinter import ttk#to add more customisation to the gui
from tkinter import scrolledtext #add a scrolled text feature to the text box
from folium.plugins import HeatMap#add a heatmap plotting function
import numpy as np #handle numbers, arrays
import webbrowser#to open maps, open internet browser
import re #regular expressin searches
from tkinter import messagebox#popup messageboxes 


##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################


win = tk.Tk()# Create instance, creates a new window of tk.Tk(win)
win.title("JSON File Analyser")# Add a title
win.wm_iconbitmap('logo.ico')#add a logo
win.configure(bg='#314e7c')#colour of window background
win.tk_strictMotif()
win.attributes('-fullscreen',True)#eable fullscreen
win.resizable(20,20)# Disable resizing the GUI


##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################



#template search, when template search button is clicked, calls this method, method checks what option is selected in dropdown 
#and calls the appropriate method relating to the selection       
def templateSearch():

   try: #add a try method to encapsulate code

    if templateChosen.get() == ("Violent Crime"):   #run the appropriate method dependig on the template chosen
        violenceSearch()
    if templateChosen.get() == ("Acquisitive Crime"):
        acquisitiveSearch()
    if templateChosen.get() == ("Criminal Damage"):
        criminalDamageSearch()
    if templateChosen.get() == ("Fraud and Forgery"):
        fraudForgerySearch()
    if templateChosen.get() == ("Drug Offences"):
        drugOffencesSearch()


#handle exceptions to give the user an idea of how to fix an error such as not selecting a file, also prevents the program from crashing
        #or just not working with no explination in the event of a problem
   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")


##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################


#regular expression search, calls this method when button is pressed, then calls the appopriate method depeding on users dropdown choice
def searchRegEx():
   try:

    if regExChosen.get() == ("@ Tags"):
        regExAt()
    if regExChosen.get() == ("Phone Numbers / ID Numbers"):
        regExPhone()

   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")





##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
#regular text search method
def search():

   try:     #try - tries this block of code, if an error occurs, instead of crashing on console, wi handle exceptions below
    searchkeyword = name.get()  # set searchKeyword to the input form text input box
    action['state'] = 'disabled'#disable search button whilst searching
    win.title("Searching For ... "+searchkeyword + "... in " + fileChosen.get() + "... Please Wait...")#change the title of window to reflect what is happening

    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645]) #create map instance
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645]) #create map instance

    from folium.plugins import MeasureControl #import measure control for maps
    map_osm.add_child(MeasureControl())#add measure control to map
    hMap.add_child(MeasureControl())


    count = 1#set counter to 1
    with open(fileChosen.get(),encoding = "utf8") as data_file: #open the file selected in dropdown with encoding utf8 (so it knows what text it will be reading)
        for row in data_file:   #treat each row seperatley and iterate through every single row
            data = json.loads(row)#set data to the entire row contents
            tempText = data['text']#tempText is equal to the tag "text" from the row
            if searchkeyword in tempText:   #If the users selected word is in the text......
                StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                scr.insert(tk.INSERT,StringToScroll)  #take several parts of the line and add it to scroll text element
                long = data['geoLocation']['longitude'] #Set long and latt from the data
                latt = data['geoLocation']['latitude']

                
                
                folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)#add a popup to the map at the location with the post number

                folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)#add marker to heatmap

                data = (np.random.normal(size=(100, 3)) *   #add location data to a map, creating a heatmap
                np.array([[0.0000001, 0.0000001,0.1 ]]) +
                np.array([[latt,long,0.5]])).tolist()

                HeatMap(data).add_to(hMap) #add heatmap data

                hMap.save(fileChosen.get() + "--" + str(searchkeyword) +' Heatmap.html') #save maps
                map_osm.save(fileChosen.get() + "--" +str(searchkeyword) + ' Search.html')
                count = count+1 #add 1 to the counter


        if count == 1: #if counter is 1 (nothing found as counter above would have been skipped)
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + str(searchkeyword))#tell the user there were no results
        else: #else, so if the counter is not 1, (will be greater than 1)
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(searchkeyword) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes': #tell the user how many results there were and ask them if they want to open the maps
                webbrowser.open_new_tab(fileChosen.get() + "--" + str(searchkeyword) +' Heatmap.html')#open the maps
                webbrowser.open_new_tab(fileChosen.get() + "--" +str(searchkeyword) + ' Search.html')
                action['state'] = 'enabled'#set button to work again and reset the title
                win.title("JSON File Analyser")
            else:#else if the user does not want to open the maps, just reset button and title
                action['state'] = 'enabled'
                win.title("JSON File Analyser")

#handle errors
   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")





##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
#template based search
def violenceSearch():

   try:
    violence = ["violence","stabbed","stabbing","knife attack","punched","assault","robbery","homicide","wounding","domestic violence","mugging","murder", "murdered","killed","manslaughter","infanticide","sexual assault","rape","drink" + "driving","drug"+"driving","GBH","possession"+"weapons","harassment","firearm","stalking"]
    #define the template words

    win.title("Searching For " +  templateChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")

    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645])
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645])

    from folium.plugins import MeasureControl
    map_osm.add_child(MeasureControl())
    hMap.add_child(MeasureControl())
#### CHOOSE FILE TO SEARCH THROUGH FROM DROPDOWN AND CALL THE CHOICE HERE
    count = 1
    with open(fileChosen.get(),encoding = "utf8") as data_file:
        for row in data_file:
            data = json.loads(row)
            tempText = data['text']
           # postText = str(data['text'])
           #for each word in the template above, determine if any word is in the text, then same as above code
            for word in violence:
                   if word in tempText:
                       StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                       scr.insert(tk.INSERT,StringToScroll)
                       long = data['geoLocation']['longitude']
                       latt = data['geoLocation']['latitude']
                       folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)

                       folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)

                       data = (np.random.normal(size=(100, 3)) *
                       np.array([[0.0000001, 0.0000001,0.1 ]]) +
                       np.array([[latt,long,0.5]])).tolist()

                       HeatMap(data).add_to(hMap)

                       hMap.save(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                       map_osm.save( fileChosen.get() + templateChosen.get()+  ' Search.html')
                       count = count+1
        if count == 1:
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + templateChosen.get())
        else:
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(templateChosen.get()) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes':
                webbrowser.open_new_tab(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                webbrowser.open_new_tab( fileChosen.get() + templateChosen.get()+  ' Search.html')
                win.title("JSON File Analyser")
            else:
                win.title("JSON File Analyser")




   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
        
def acquisitiveSearch():

   try:
    acquisitive = ["theft","burglary","vehicle"+"stolen","nicked","robbery","breaking"+"entering","bike"+"stolen"]



    win.title("Searching For " +  templateChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")

    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645])
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645])

    from folium.plugins import MeasureControl
    map_osm.add_child(MeasureControl())
    hMap.add_child(MeasureControl())
#### CHOOSE FILE TO SEARCH THROUGH FROM DROPDOWN AND CALL THE CHOICE HERE
    count = 1
    with open(fileChosen.get(),encoding = "utf8") as data_file:
        for row in data_file:
            data = json.loads(row)
            tempText = data['text']
           # postText = str(data['text'])
            for word in acquisitive:
                   if word in tempText:
                       StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                       scr.insert(tk.INSERT,StringToScroll)
                       long = data['geoLocation']['longitude']
                       latt = data['geoLocation']['latitude']
                       folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)

                       folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)

                       data = (np.random.normal(size=(100, 3)) *
                       np.array([[0.0000001, 0.0000001,0.1 ]]) +
                       np.array([[latt,long,0.5]])).tolist()

                       HeatMap(data).add_to(hMap)

                       hMap.save(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                       map_osm.save( fileChosen.get() + templateChosen.get()+  ' Search.html')
                       count = count+1

        if count == 1:
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + templateChosen.get())
        else:
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(templateChosen.get()) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes':
                webbrowser.open_new_tab(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                webbrowser.open_new_tab( fileChosen.get() + templateChosen.get()+  ' Search.html')
                win.title("JSON File Analyser")
            else:
                win.title("JSON File Analyser")

   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")




##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
        
        
def criminalDamageSearch():

   try:

    criminalDamage = ["vandalism","vandalised","vandal","arson","graffiti","deliberate damage","malicious","set fire", "criminal damage","destroyed","damaged","keying"+"car","reckless"]



    win.title("Searching For " +  templateChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")

    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645])
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645])

    from folium.plugins import MeasureControl
    map_osm.add_child(MeasureControl())
    hMap.add_child(MeasureControl())
#### CHOOSE FILE TO SEARCH THROUGH FROM DROPDOWN AND CALL THE CHOICE HERE
    count = 1
    with open(fileChosen.get(),encoding = "utf8") as data_file:
        for row in data_file:
            data = json.loads(row)
            tempText = data['text']
           # postText = str(data['text'])
            for word in criminalDamage:
                   if word in tempText:
                       StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                       scr.insert(tk.INSERT,StringToScroll)
                       long = data['geoLocation']['longitude']
                       latt = data['geoLocation']['latitude']
                       folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)

                       folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)

                       data = (np.random.normal(size=(100, 3)) *
                       np.array([[0.0000001, 0.0000001,0.1 ]]) +
                       np.array([[latt,long,0.5]])).tolist()

                       HeatMap(data).add_to(hMap)

                       hMap.save(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                       map_osm.save( fileChosen.get() + templateChosen.get()+  ' Search.html')
                       count = count+1

        if count == 1:
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + templateChosen.get())
        else:
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(templateChosen.get()) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes':
                webbrowser.open_new_tab(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                webbrowser.open_new_tab( fileChosen.get() + templateChosen.get()+  ' Search.html')
                win.title("JSON File Analyser")
            else:
                win.title("JSON File Analyser")



   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
        
def fraudForgerySearch():

   try:


    fraudForgery = ["fraud","forgery","identity theft","bank card"+"stolen", "false accounting","bankruptcy", "credit card","debit card","bank details"+"stolen", "fraudulent"]



    win.title("Searching For " +  templateChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")


    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645])
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645])

    from folium.plugins import MeasureControl
    map_osm.add_child(MeasureControl())
    hMap.add_child(MeasureControl())
#### CHOOSE FILE TO SEARCH THROUGH FROM DROPDOWN AND CALL THE CHOICE HERE
    count = 1
    with open(fileChosen.get(),encoding = "utf8") as data_file:
        for row in data_file:
            data = json.loads(row)
            tempText = data['text']
           # postText = str(data['text'])
            for word in fraudForgery:
                   if word in tempText:
                       StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                       scr.insert(tk.INSERT,StringToScroll)
                       long = data['geoLocation']['longitude']
                       latt = data['geoLocation']['latitude']
                       folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)

                       folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)

                       data = (np.random.normal(size=(100, 3)) *
                       np.array([[0.0000001, 0.0000001,0.1 ]]) +
                       np.array([[latt,long,0.5]])).tolist()

                       HeatMap(data).add_to(hMap)

                       hMap.save(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                       map_osm.save( fileChosen.get() + templateChosen.get()+  ' Search.html')
                       count = count+1

        if count == 1:
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + templateChosen.get())
        else:
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(templateChosen.get()) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes':
                webbrowser.open_new_tab(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                webbrowser.open_new_tab( fileChosen.get() + templateChosen.get()+  ' Search.html')
                win.title("JSON File Analyser")
            else:
                win.title("JSON File Analyser")

   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")




##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
        

def drugOffencesSearch():

   try:

    drugOffences = ["drugs", "drug"+ "possession","intent to supply","cannabis","class a","class b", "class c","drug trafficking", "heroin","cocaine","LSD","amphetamine","ketamine"]



    win.title("Searching For " +  templateChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")


    map_osm = folium.Map(location=[53.472328361821766,-2.23959064483645])
    hMap = folium.Map(location=[53.472328361821766,-2.23959064483645])

    from folium.plugins import MeasureControl
    map_osm.add_child(MeasureControl())
    hMap.add_child(MeasureControl())
#### CHOOSE FILE TO SEARCH THROUGH FROM DROPDOWN AND CALL THE CHOICE HERE
    count = 1
    with open(fileChosen.get(),encoding = "utf8") as data_file:
        for row in data_file:
            data = json.loads(row)
            tempText = data['text']
           # postText = str(data['text'])
            for word in drugOffences:
                   if word in tempText:
                       StringToScroll = "\n\n["+str(count)+"]" + "\n----------------- \nDate: " + data['createdAt']['$date'] + " \nLatitude:" + str(data['geoLocation']['latitude']) + " \nLongitude:" + str(data['geoLocation']['longitude']) + "\nTweet Text:" + data['text']+"Platform: " + "\nPost Source: " + data['source'] 
                       scr.insert(tk.INSERT,StringToScroll)
                       long = data['geoLocation']['longitude']
                       latt = data['geoLocation']['latitude']
                       folium.Marker([latt,long], popup = "Post " + str(count)).add_to(map_osm)

                       folium.CircleMarker([latt, long],popup="Post "+ str(count),fill_color="#3db7e4",).add_to(hMap)

                       data = (np.random.normal(size=(100, 3)) *
                       np.array([[0.0000001, 0.0000001,0.1 ]]) +
                       np.array([[latt,long,0.5]])).tolist()

                       HeatMap(data).add_to(hMap)

                       hMap.save(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                       map_osm.save( fileChosen.get() + templateChosen.get()+  ' Search.html')
                       count = count+1


        if count == 1:
            messagebox.showinfo("Finished", "File Searched, No Results Found For " + templateChosen.get())
        else:
            result = messagebox.askquestion("Finished", "File Searched, "+ str(count-1) + " Results For " + str(templateChosen.get()) + "\n\nWould You Like To Open The Plotted Maps?\n\n (Maps Saved In File Directory)")
            if result == 'yes':
                webbrowser.open_new_tab(fileChosen.get()  + templateChosen.get()+  ' Heatmap.html')
                webbrowser.open_new_tab( fileChosen.get() + templateChosen.get()+  ' Search.html')
                win.title("JSON File Analyser")
            else:
                win.title("JSON File Analyser")


   except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")


        
 
##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        

#regular expression for @ tags / email addresses
def regExAt():

  try:

   win.title("Searching For " +  regExChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")
   text = open(fileChosen.get(),encoding = "utf8") #open the chosen file and read it in utf8
   search = re.compile('(@[\w\.-]+)') #search using the regular expression, looking for the @ symbol with characters after it
   searches = search.findall(text.read())#search for all matches


   if search:
           StringToScroll = "\n\n" + str(searches)#if matches occur, insert to scroll
           scr.insert(tk.INSERT,StringToScroll)
           messagebox.showinfo("Finished", "File Searched, Showing " + regExChosen.get() + " Terms in " + fileChosen.get())
   else:    #if no matches, tell user
           StringToScroll = "\n\nNothing Found"
           scr.insert(tk.INSERT,StringToScroll)
           messagebox.showinfo("Finished", "File Searched, No Results Found For " + regExChosen.get() + " Terms in " + fileChosen.get())


  except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
  except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
  except EOFError:
        messagebox.showerror("Error", "EOF Error")
  except:
        messagebox.showerror("Error", "Error Occured")



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
        

def regExPhone():

  try:

   win.title("Searching For " +  regExChosen.get() + " Terms in " + fileChosen.get() + "... Please Wait...")
   text = open(fileChosen.get(),encoding = "utf8")
   search = re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
   #regular expression to find possible phone numbers / ID numbers
   searches = search.findall(text.read())

   if search:
           StringToScroll = "\n\n" + str(searches)
           scr.insert(tk.INSERT,StringToScroll)
           messagebox.showinfo("Finished", "File Searched, Showing Possible " + regExChosen.get() + " in " + fileChosen.get())
   else:
           StringToScroll = "\n\nNothing Found"
           scr.insert(tk.INSERT,StringToScroll)
           messagebox.showinfo("Finished", "File Searched, No Results Found For " + regExChosen.get() + " Terms in " + fileChosen.get())

  except IOError:
        messagebox.showwarning("Error", "IO Error! \n\n Could Not Read / Find File, Ensure You Have Selected One!")
  except ImportError:
        messagebox.showerror("Error", "Import Error! \n\Could Not Loading Module")
  except EOFError:
        messagebox.showerror("Error", "EOF Error")
  except:
        messagebox.showerror("Error", "Error Occured")



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
#delete method, clears text from screen if button clicked
def delete():

   try:#try to open a message bx telling user the text has been deleted then clear text box
      result = messagebox.askquestion("Clear Text", "Are You Sure You Want To Remove All Text?")
      if result == 'yes':
          messagebox.showinfo("Removing Text", "All Text Removed")
          scr.delete(1.0,END)
      
      #if cannot clear box, tell user the error

   except IOError:
        messagebox.showwarning("Error", "Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Error Whilst Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")

##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        
        
#define exit method, simpley closes the programe if the user clicks exit
def exit():
    
   try:
        result = messagebox.askquestion("Exit", "Are You Sure You Want To Exit?")
        if result == 'yes':
            win.destroy()
            
            
            
   except IOError:
        messagebox.showwarning("Error", "Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Error Whilst Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")
            
    



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################

# Changing our Label
ttk.Label(win, text="Enter a keyword to search:").grid(column=2, row=2)
# Adding a Textbox Entry widget
name = tk.StringVar()
nameEntered = ttk.Entry(win, width=40, textvariable=name)
nameEntered.grid(column=2, row=4)




##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################


def toggle(*_):
    if name.get():
        action1['state'] = 'normal'
    else:
        action1['state'] = 'disabled'
        



##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################
        

        
        
#define exit method, simpley closes the programe if the user clicks exit
def help():
    
   try:
        messagebox.showinfo("Help", "Welcome To JSON Analyser\n\n [1] To Begin, You Need To Select A File You Would Like To Search Using The Dropdown At The Top Left Of The Screen \n\n [2] Once You Have Selected A File, You Are Ready To Begin Analysing! \n\n [3] Keyword Search - Useful If You Have A Particular Word You Are Looking For, Will Scan The File For Your Chosen Word \n\n [4] Template Searching - Choose From A Predefined List Of Crime Types, File WIll Be Scanned For Possible Crimes \n\n [5] Regular Expression Searching, Useful For Trying To FInd Particular Types Of Data, Can Pick Out ID Numbers, Phone Numbers, Email Addresses / @ Tags. \n\n When Carrying Out A Template Search Or Keyword Search, You Will Be Asked If You Would Like To Open A Map, Thats Right! JSON Analyser Will Create A Heatmap And Plotted Point Map To Make Your Life Easy! Maps Are Saved In File Directory \n\nThank You For Using JSON Analyser! ")
      
        
            
            
   except IOError:
        messagebox.showwarning("Error", "Could Not Read / Find File, Ensure You Have Selected One!")
   except ImportError:
        messagebox.showerror("Error", "Error Whilst Loading Module")
   except EOFError:
        messagebox.showerror("Error", "EOF Error")
   except:
        messagebox.showerror("Error", "Error Occured")
        


##############################################################################################################
####################################BOTTOM####################################################################

name.trace_add('write', toggle)


action2 = ttk.Button(win, text="Clear Text From Screen!", command=delete)
action2.grid(column=10, row = 15, columnspan = 10, pady = 20)

action2 = ttk.Button(win, text="Exit", command=exit)
action2.grid(column=3, row = 15, columnspan = 10, pady = 20)

action2 = ttk.Button(win, text="Help Guide", command=help)
action2.grid(column=1, row = 15, columnspan = 5, pady = 20)



##############################################################################################################
##################################TOP#########################################################################


action1 = ttk.Button(win, text="Search For Keyword Hits", command=search, state = 'disabled')
action1.grid(column=2,row=5 , padx=10, pady=10)


# Adding a buttons
action = ttk.Button(win, text="Search Using Template", command=templateSearch, state = 'normal')
action.grid(column=7,row=5 , padx=10, pady=10)



action3 = ttk.Button(win, text="Search Using Regular Expression", command=searchRegEx, state = 'normal')
action3.grid(column=13,row=5 , padx=10, pady=10)




##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################



ttk.Label(win, text="Select A JSON File To Use:").grid(column=0, row=0)
file = tk.StringVar()
fileChosen = ttk.Combobox(win, width=40, textvariable=str)
fileChosen['values'] = ('Manchester_Part-1.json', 'Manchester_Part-2.json', 'Manchester_Part-3.json', 'Sample-2-Tweets.json','sample.json')
fileChosen.grid(column=0, row=1)
fileChosen.current(4)



ttk.Label(win, text="Select A Template Based Search:").grid(column=7, row=2)
file = tk.StringVar()
templateChosen = ttk.Combobox(win, width=40, textvariable=str)
templateChosen['values'] = ('Violent Crime', 'Acquisitive Crime', 'Criminal Damage', 'Fraud and Forgery' , 'Drug Offences')
templateChosen.grid(column=7, row=4)



ttk.Label(win, text="Select A Reular Expression To Search:").grid(column=13, row=2)
file = tk.StringVar()
regExChosen = ttk.Combobox(win, width=40, textvariable=str)
regExChosen['values'] = ('@ Tags', 'Phone Numbers / ID Numbers')
regExChosen.grid(column=13, row=4)



ttk.Label(win, text="JSON Analyser", background = "#448628", font = "times 20 bold").grid(column=6, row=0, columnspan = 2)




##############################################################################################################
##############################################################################################################
##############################################################################################################        
##############################################################################################################
##############################################################################################################



# Using a scrolled Text control
scrolW = 120
scrolH = 30
scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=1, columnspan=20, row = 6, pady = 20)

messagebox.showinfo("Welcome!", "Welcome To JSON Analyser! \n\n Click On Help At The Bottom Of The Screen For Instructions")

# Place cursor into name Entry
nameEntered.focus()
#======================
# Start GUI
#======================
win.mainloop()

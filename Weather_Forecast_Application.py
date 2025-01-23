import requests #this library in python enables us to connect to api as an HTTP client

api_url = "https://api.openweathermap.org/data/2.5/weather"

api_key = "xxxxxxxxxxx" #hardcoding the api to variable helps ensure accuracy

def get_coordinates(location): #first call requirement
    url = f"{api_url}?q={location}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "coord" in data:
            latitude = data["coord"]["lat"]
            longitude = data["coord"]["lon"]
            return latitude, longitude
        else:
            return None
    except requests.exceptions.RequestException as error:
        print("Error getting coordinates: {error} .Please try again")
        return None

def get_weather_data(latitude, longitude): #second call requirement
    url = f"{api_url}?lat={latitude}&lon={longitude}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print("Error getting weather information: {error} .Please try Again.")
        return None

def get_loc(loc_options): #function allows user to pass location requirements for weather inquiry
    if loc_options.lower() == "city":
        city_input = input("\nEnter city: ").lower()
        state_input = input("\nEnter state: ").lower()
        location_input = f"{city_input},{state_input}"
    elif loc_options.lower() == "zip":
        location_input = input("\nEnter zip code: ")
        country_input = input("\nEnter country code. (For United States, enter (US): ").upper()
        location_input += f",{country_input}"
    else:
        location_input = None

    return location_input

def temp_conversion(temp_options,temp): #function allows user to choose units for temperature display

    if temp_options.lower() == 'c':
        return temp - 273.15
    elif temp_options.lower() == 'f':
        return (temp - 273.15) * 9/5 + 32
    elif temp_options.lower() == 'k':
        return temp
    else:
        print("Invalid unit choice. Please choose C, F, or K.")
        return

def main(): #main function calls & implements other functions in the program
    print("\nHello and Thank you for using the DSC510 Weather Forecast App!")

    while True:
        loc_options = input('''
        Select the type of lookup for the location for your weather inquiry.
        Type city to lookup by city & state,
        Type zip to lookup by Zip and Country Code
        or Type quit to end the program: ''')

        if loc_options.lower() == "quit":
            print("Thank you for using the DSC510 Weather Program. Have a great day!")
            break
        elif loc_options.lower() in ["city", "zip"]:
            location_input = get_loc(loc_options)  # Get location information

            if location_input is None:
                print("Invalid choice. Please choose city, zip, or quit.")
                continue

            coordinates = get_coordinates(location_input)

            if coordinates:
                latitude, longitude = coordinates
                weather_data = get_weather_data(latitude, longitude)
                if weather_data:
                    if "main" in weather_data and "weather" in weather_data:
                        main_info = weather_data["main"]
                        weather_info = weather_data["weather"][0]

                        location_name = weather_data["name"]
                        temp_default = main_info["temp"]
                        feels_like_default = main_info["feels_like"]
                        temp_min_default = main_info["temp_min"]
                        temp_max_default = main_info["temp_max"]
                        pressure = main_info["pressure"]
                        humidity = main_info["humidity"]
                        weather_description = weather_info["description"]


                        # Convert temperatures using the temp_conversion functions
                        temp_options = input('''
                                        How would you like your temperature options displayed?
                                         Enter C for Celsius
                                         Enter F for  Farenheit
                                         Enter K for Kelvin
                                         Enter temperature option: ''')
                        if temp_options.lower() == "c":
                            current_temp = temp_conversion("c",temp_default)
                            feels_like_temp = temp_conversion("c",feels_like_default)
                            low_temp = temp_conversion("c",temp_min_default)
                            high_temp = temp_conversion("c",temp_max_default)
                            unit_symbol = " C"
                        elif temp_options.lower() == "f":
                            current_temp = temp_conversion("f",temp_default)
                            feels_like_temp = temp_conversion("f",feels_like_default)
                            low_temp = temp_conversion("f",temp_min_default)
                            high_temp = temp_conversion("f",temp_max_default)
                            unit_symbol = " F"
                        else:
                            current_temp = temp_default
                            feels_like_temp = feels_like_default
                            low_temp = temp_min_default
                            high_temp = temp_max_default
                            unit_symbol = "K"

                        # Putting it all together to print out information for user based on requirements
                        print\
                        (f"""
                        What's the weather like in {location_name}?
                        {weather_description}
                        Current Temperature: {current_temp:.2f} {unit_symbol}
                        Feels Like Temperature: {feels_like_temp:.2f} {unit_symbol}
                        Low Temperature: {low_temp:.2f} {unit_symbol}
                        High Temperature: {high_temp:.2f} {unit_symbol}
                        Pressure: {pressure}
                        Humidity: {humidity}
                        """)
                    else:
                        print("Weather data not found. Please check the location or try again.\n")
            else:
                print("Coordinates not found for the given location. Please check the location or try again.\n")
        else:
            print("Invalid choice. Please choose city, zip, or quit.")

if __name__ == "__main__":
    main()

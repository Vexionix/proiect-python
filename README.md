# **STATES OF THE WORLD**

This Python project scrapes data about countries from Wikipedia, stores the information in a SQLite database, and exposes it via a Flask REST API. <br><br>
Via the API the users can extract the following data: the top 10 countries by population/area/density, the capital for a specific country, which countries speak a specific language or follow a political system (regime) or countries that fit a timezone etc.

---

## **Features**

- **Data Scraping:**
  Scrapes details such as population, density, area, capital, language, timezone, neighboring countries, and political regime from Wikipedia.
- **Data Storage:**
  Stores the scraped data in a SQLite database.
- **REST API:**
  Offers endpoints for querying country data.

---

## **API Endpoints**

### **1. Top 10 Countries by Population**
- **Endpoint**: `/top-10-tari-populatie`
- **Method**: `GET`
- **Description**: Returns the top 10 countries with the highest population.
- **Response Example**:
  ```json
  [
      { "name": "India", "population": 1425775850 },
      { "name": "China", "population": 1411750000 },
      ...
  ]
  ```

### **2. Top 10 Countries by Population Density**
- **Endpoint**: `/top-10-tari-densitate`
- **Method**: `GET`
- **Description**: Returns the top 10 countries with the highest population density.
- **Response Example**:
  ```json
  [
    { "name": "Macau", "people per km² (density)": 21411 },
    { "name": "Monaco", "people per km² (density)": 18175 },
    ...
  ]
  ```

### **3. Top 10 Countries by Area**
- **Endpoint**: `/top-10-tari-suprafata`
- **Method**: `GET`
- **Description**: Returns the top 10 countries with the largest area in km².
- **Response Example**:
  ```json
  [
    { "area (km²)": 17075400, "name": "Rusia" },
    { "area (km²)": 9984670, "name": "Canada" },
    ...
  ]
  ```


### **4. Countries by Timezone**
- **Endpoint**: `/tarile-cu-fus-orar`
- **Method**: `GET`
- **Query Parameters**:
    - `fus_orar`: (string) Timezone to match, case-insensitive.
- **Description**: Returns countries that match the given timezone.
- **Example Request**: /tarile-cu-fus-orar?fus_orar=-4
- **Response Example**:
  ```json
  [
    { "name": "Venezuela" },
    { "name": "Chile" },
    ...
  ]
  ```

### **5. Countries by Language**
- **Endpoint**: `/tarile-care-vorbesc`
- **Method**: `GET`
- **Query Parameters**:
    - `limba`: (string) The language spoken by countries, case-insensitive.
- **Description**: Returns countries where the given language is spoken.
- **Example Request**: /tarile-care-vorbesc?limba=chineza
- **Response Example**:
  ```json
  [
    {"name": "China"},
    {"name": "Republica China (Taiwan)"},
    ...
  ]
  ```

### **6. Countries by Political System (Regime)**
- **Endpoint**: `/tarile-cu-sistem-politic`
- **Method**: `GET`
- **Query Parameters**:
    - `sistem_politic`: (string) The political system (regime) to match, case-insensitive.
- **Description**: Returns countries matching the given political system (regime).
- **Example Request**: /tarile-cu-sistem-politic?sistem_politic=monarhie
- **Response Example**:
  ```json
  [
    { "name": "Japonia" },
    { "name": "Regatul Unit" },
    ...
  ]
  ```

### **7. Neighbors of a Country**
- **Endpoint**: `/tarile-vecine-pentru`
- **Method**: `GET`
- **Query Parameters**:
    - `tara`: (string) The name of the country to retrieve neighbors for, case-insensitive.
- **Description**: Returns the neighbors of the given country.
- **Example Request**: /tarile-vecine-pentru?tara=China
- **Response Example**:
  ```json
  [
    { "neighbors": "Mongolia / Kazahstan / Kargazstan / Tadjikistan / Pakistan / India / Nepal / Bhutan / Myanmar / Laos / Vietnam / Rusia / Coreea de Nord / Afganistan / Coreea de Sud / Japonia" }
  ]
  ```

### **8. Capital of a Country**
- **Endpoint**: `/capitala-tarii`
- **Method**: `GET`
- **Query Parameters**:
    - `tara`: (string) The name of the country to retrieve the capital for, case-insensitive.
- **Description**: Returns the capital of the given country.
- **Example Request**: /capitala-tarii?tara=Japonia
- **Response Example**:
  ```json
  [
    { "capital": "Tokyo" }
  ]
  ```
  
---

## **Known Issues**

1. **Website Dependency**:
   - Relies on Wikipedia's page structure; updates to the HTML structure may break functionality.
   
2. **Inconsistencies in Scraped Data**:
   - Not all countries have complete data in Wikipedia. Example: Transnistria
   - Not all fields follow the same formatting rules, some numbers are written in such a way that it might break formatting and is unavoidable. For example: "144.440" can mean 144440 or 144,44 and it's indistinguishable.

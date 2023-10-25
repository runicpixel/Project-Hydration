#include <Firebase_Arduino_WiFiNINA.h>
#include <RTCZero.h> // Include RTCZero library for real-time clock

const char ssid[] = "Hardik";
const char pass[] = "h@628323";
const String DATABASE_URL = "gsr-89764-default-rtdb.firebaseio.com";
const String DATABASE_SECRET = "Iq1gFhTAsPvoLCvLsMv6Xd5yu8VwKoUSF69Bf3nt";

const int GSR = A0;
int threshold = 0;
int sensorValue;

FirebaseData firebaseData;

RTCZero rtc; // Initialize the RTCZero object

void setup() {
  Serial.begin(9600);

  Serial.println("Connecting to Wi-Fi");
  int status = WL_IDLE_STATUS;

  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    Serial.print(".");
    delay(100);
  }

  Firebase.begin(DATABASE_URL, DATABASE_SECRET, ssid, pass);
  Firebase.reconnectWiFi(true);

  rtc.begin(); // Initialize the RTC
  if (!rtc.isConfigured()) {
    rtc.setEpoch(0); // Set the RTC to the current time if not configured
  }

  Serial.println("Connected");
}

void loop() {
  // Get the current time from the RTC
  int year = rtc.getYear();
  int month = rtc.getMonth();
  int day = rtc.getDay();
  int hour = rtc.getHours();
  int minute = rtc.getMinutes();
  int second = rtc.getSeconds();

  // Construct the Firebase path
  String firebasePath = "/users/month" + String(month) + "/day" + String(day) + "/gsr";

  for (int i = 0; i < 1000; i++) {
    sensorValue = analogRead(GSR);
    threshold += sensorValue;
    delay(5);
  }
  threshold /= 1000;
  Serial.print("threshold = ");
  Serial.println(threshold);

  if(threshold>=400)
  {
    Serial.println("Dehydrated");
  }
  else if(threshold<400 && threshold>=200)
  {
    Serial.println("Mildy Dehydrated");
  }
  else
  {
    Serial.println("Hwydrated");
  }

  // Send the GSR data to Firebase under the constructed path
  Firebase.setInt(firebaseData, firebasePath, threshold);

  if (firebaseData.dataAvailable()) {
    Serial.println("Data sent");
  } else {
    Serial.println("Failed");
    Serial.println(firebaseData.errorReason());
  }
  delay(1000);
}

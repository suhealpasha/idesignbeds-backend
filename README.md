# Python Vendor API

## Vendor user lab launching api 

###### URL : **/v1/launch/lab**

##### Request : POST

###### Header
```javascript
{
    "X-API-KEY" : <x-api-key>
}

```

###### Body

```javascript
{
    "username" : <vendor_username>,
    "password": <vendor_password>,
    "lab": <lab_id>
}
```

##### Response

######  Status 200
```javascript
{
    "lab": <string data which contains lab URL>
}

```
###### Status other than 200

```javascript
{
    "Error": <error message>
}
```

## Moodle user lab launching api 

###### URL : **/v1/lab/moodle**

##### Request : POST

###### Header
```javascript
{
    "X-API-KEY" : <x-api-key>
}

```

###### Body

```javascript
{
    "user_name" : <vendor user name>,
    "course_name": <course name>,
    "lab": <lab name>
}
```

##### Response

######  Status 200
```javascript
{
    "lab": <string data which contains lab URL>
}

```
###### Status other than 200

```javascript
{
    "Error": <error message>
}
```

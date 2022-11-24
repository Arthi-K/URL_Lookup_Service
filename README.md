# URL_Lookup_Service

Functional Requirements: 
The caller passes in a URL and the service should respond with some information about that URL. 
The caller wants to know if it safe to access that URL or not 
The URL passed in by the caller should be checked in the databases of malware URLs if the resource being requested is known to contain malware

Non-functional requirements: 
These lookups are blocking users from accessing the URL until the caller receives a response from your service, which denotes that the response time should be quick. Also a particular requested URL can be cached in order to give faster response rather than making a call to DB every time. 
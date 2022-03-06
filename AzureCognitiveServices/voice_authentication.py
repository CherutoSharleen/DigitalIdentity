import requests

SUBSCRIPTION_KEY = '2a6adfbe095b4e058c4ecf310350cce6'
ENDPOINT = 'https://eastus.api.cognitive.microsoft.com'

# Create a profile that will be associated with a user
def create_profile():

	headers = {
	    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	    'Content-Type': 'application/json',
	}

	data = '{"locale":"en-us"}'

	response = requests.post('%s/speaker/verification/v2.0/text-independent/profiles'%ENDPOINT, headers=headers, data=data)
	response = response.json()

	profile_id = response["profileId"]

	return profile_id


# Add user voice to profile created
def enroll(profile_id, file_path):

	headers = {
	    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	    'Content-Type': 'audio/wav',
	}

	data = open(file_path, 'rb').read()
	response = requests.post('%s/speaker/verification/v2.0/text-independent/profiles/%s/enrollments'%(ENDPOINT, profile_id), headers=headers, data=data)

	response = response.json()

	status = response["enrollmentStatus"]

	if status == "Enrolled":
		print(profile_id , ": Enrollment succesful")

	else:
		print(profile_id , ": Enrollment failed")

	return status

# Verify user
def verify(profile_id, file_path):

	headers = {
	    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
	    'Content-Type': 'audio/wav',
	}

	data = open(file_path, 'rb').read()
	response = requests.post('%s/speaker/verification/v2.0/text-independent/profiles/%s/verify'%(ENDPOINT, profile_id), headers=headers, data=data)

	response = response.json()
	
	result = response["recognitionResult"]

	if result == "Accept":
		print("Authentication Passed")

	else:
		print("Authentication Failed")

	return result


if __name__ == '__main__':

	mode = "verify"

	# Verify user voice
	if mode == "verify":
		profile_id = "daf0e1ed-83b9-45f0-82b4-9fbc21bfd338"
		file_path = 'Samples/leslie_testing.wav'
		verify(profile_id, file_path)

	# Enroll user voice
	elif mode == "enroll":
		profile_id = create_profile()
		file_path = 'Samples/leslie.wav'
		enroll(profile_id, file_path)
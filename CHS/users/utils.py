import gmaps
from django.contrib.gis.geoip2 import GeoIP2
import gmaps.datasets
import face_recognition
from models import Profile

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geo(ip):
    g = GeoIP2()
    lat, lon = g.lat_lon(ip)
    return lat, lon

def get_zoom(distance):
    if distance <=100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2

def get_face_id(unknown):   #unknown is image file
    unknown_picture = face_recognition.load_image_file(unknown)
    unknown_face_encodings = face_recognition.face_encodings(unknown_picture)

    known_pictures = Profile.objects.face_picture
    known_face_ids = Profile.objects.aadhar_uid
    known_face_encodings = []
    for known_picture in known_pictures:
        known_face_encodings.append(face_recognition.face_encodings(known_picture)[0])
    face_ids = []
    for unknown_face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_ids[best_match_index]

        face_ids.append(name)
    return face_ids

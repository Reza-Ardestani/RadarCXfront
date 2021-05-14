from najva_api_client.najva import Najva
client = Najva()

client.apikey = "9e48e9f0-41e1-4f0a-a3d0-dd34b8313f03"
client.token = "6e83d4164baf569f345ab556b01347b1178776c5"

str = client.send_to_users(title="fuck",body="Some Description", url="https://google.com",
icon="https://www.ait-themes.club/wp-content/uploads/cache/images/2020/02/guestblog_featured/guestblog_featured-482918665.jpg",
image="https://www.ait-themes.club/wp-content/uploads/cache/images/2020/02/guestblog_featured/guestblog_featured-482918665.jpg",
onclick="open-link", 
subscriber_tokens=['67a4f40e-dba4-421d-be7e-ef40261584a5', ])

print(str)
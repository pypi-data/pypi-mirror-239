from aistore import Client

client = Client("http://localhost:8080")

props, summ = client.bucket(bck_name="testpyaisloader", provider="ais").info()

# print("Props: " + props)
print(summ)
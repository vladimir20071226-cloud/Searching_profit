STATUS=[("profitable", "выгодный"), ("doubtful", "сомнительно"), ("unprofitable", "невыгодно")]
dictionary=dict(STATUS)
for key, value in dictionary.items():
    print(len(key))
    print(len(value))


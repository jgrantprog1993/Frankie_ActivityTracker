import BlynkLib

BLYNK_AUTH = '_1YBrbat_TJksBX_p4ni9jz5gr3q62so'
# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# register handler for virtual pin V0 write event
@blynk.on("V0")
def v3_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')

# infinite loop that waits for event
while True:
    blynk.run()
    blynk.virtual_write()
    pass
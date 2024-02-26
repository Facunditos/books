import requests,time

print('¡Bienvenidos!')
servidor_direccion_ip = input("Ingrese la dirección IP del servidor: ")

def libro()->dict:
    author = input("Autor: ")
    country = input("País: ")
    imageLink = input("Foto: ")
    language = input("Idioma: ")
    link = input("Enlace: ")
    pages = int(input("Cantidad de páginas: "))
    title = input("Título: ")
    year = int(input("Año: "))
    libro = {
      "author": author,
      "country": country,
      "imageLink": imageLink,
      "language": language,
      "link": link,
      "pages": pages,
      "title": title,
      "year": year
    }   
    return libro

def imprimir_libro(libro:dict)->None:
    autor = libro['author']
    pais = libro['country']
    imagen = libro['imageLink']
    idioma = libro['language']
    enlace = libro['link']
    paginas = libro['pages']
    titulo = libro['title']
    año = libro['year']
    print(f"* {titulo}")
    print(f"\t autor: {autor}")
    print(f"\t pais: {pais}")
    print(f"\t imagen: {imagen}")
    print(f"\t idioma: {idioma}")
    print(f"\t enlace: {enlace}")
    print(f"\t paginas: {paginas}")
    print(f"\t año: {año}")

def menu()->int:
    print("--------------------------------------")
    print("\nIngrese una de las siguientes opciones")
    print("1- Buscar todos los libros")
    print("2- Agregar un libro")
    print("3- Buscar un libro por título")
    print("4- Buscar libros por autor")
    print("5- Editar un libro")
    print("6- Eliminar un libro")
    print("0- Salir")
    op = input("Ingrese la opción deseada: ")
    while(not op.isdigit() or int(op)<0 or int(op)>6):
        op = (input("Error. Vuelva a ingresar una opción (0-6): "))
    return int(op)

def repetir_menu():
  repetir_menu = input("\n¿Quiere repetir el menú? (sí-no): ")
  if (repetir_menu=="no"):
    op=0
    return op
  
def buscar_libros()->None:
    respuesta = requests.get(f"http://{servidor_direccion_ip}:80/api/v1/books")
    if (respuesta.status_code==200):
      libros = respuesta.json()
      print(f'\nContamos con los siguiente {len(libros)} libros:\n')
      for libro in libros:
        imprimir_libro(libro)
    elif (respuesta.status_code==404):
        print("No tenemos libros para mostrar")    

  
def crear_libro(nuevo_libro:dict)->None:
  respuesta = requests.post(f"http://{servidor_direccion_ip}:80/api/v1/books/",json=nuevo_libro)
  if (respuesta.status_code==201):
    libro_creado = respuesta.json()
    print("Agregamos el siguiente libro: \n")
    imprimir_libro(libro_creado)

def buscar_libro_titulo(titulo:str)->None:
    respuesta = requests.get(f"http://{servidor_direccion_ip}:80/api/v1/books/{titulo}")
    if (respuesta.status_code==200):
        libro = respuesta.json()
        print(f'\nEste es el libro que encontramos con ese título:\n')
        imprimir_libro(libro)
    elif (respuesta.status_code==404):
        print("No tenemos ningún libro con ese título")
        
def buscar_libros_autor(autor:str)->None:
  autor_buscado = {"author":autor}
  #El argumento params almacena la query de la solicitud
  respuesta = requests.get(f"http://{servidor_direccion_ip}:80/api/v1/books/search",params=autor_buscado)
  if (respuesta.status_code==200):
    libros = respuesta.json()
    print("Contamos con los siguientes libros de ese autor: \n")
    for libro in libros:
      imprimir_libro(libro)
  elif (respuesta.status_code==404):
      print("No tenemos libros de ese autor")


def actualizar_libro(titulo:str,libro_editado:str)->None:
  respuesta = requests.put(f"http://{servidor_direccion_ip}:80/api/v1/books/{titulo}",json=libro_editado)
  if (respuesta.status_code==200):
      libro = respuesta.json()
      print("Libro actualizado: \n")
      imprimir_libro(libro)
  elif (respuesta.status_code==404):
      print("No tenemos ningún libro con ese título")
  
def eliminar_libro(titulo:str)->None:
  respuesta = requests.delete(f"http://{servidor_direccion_ip}:80/api/v1/books/{titulo}")
  if (respuesta.status_code==200):
      print("Libro eliminado")
  elif (respuesta.status_code==404):
      print("No tenemos ningún libro con ese título")

def principal():
  opcion=1
  while opcion!=0:
    opcion = menu()
    if (opcion==1):
      buscar_libros()
      time.sleep(3)
      opcion = repetir_menu()
    if (opcion==2):
      nuevo_libro = libro()
      crear_libro(nuevo_libro)   
      time.sleep(3) 
      opcion = repetir_menu()
    if (opcion==3):
      titulo = input("Ingrese el título del libro que desea buscar: ")
      buscar_libro_titulo(titulo)
      time.sleep(3)
      opcion = repetir_menu()
    if (opcion==4):
      autor = input("Ingrese el autor que desea buscar: ")
      buscar_libros_autor(autor) 
      time.sleep(3)
      opcion = repetir_menu() 
    if (opcion==5):
      libro_actualizado = libro()
      titulo_libro_actualizado = libro_actualizado['title']
      actualizar_libro(titulo_libro_actualizado,libro_actualizado)
      time.sleep(3)
      opcion = repetir_menu()
    if (opcion==6):
      titulo_libro_eliminado = input("Ingrese el título del libro que desea eliminar: ")
      eliminar_libro(titulo_libro_eliminado) 
      time.sleep(3)
      opcion = repetir_menu()
  print("Fin del programa!")  

principal()



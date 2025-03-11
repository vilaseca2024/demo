from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from multiprocessing import AuthenticationError
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now
from django.http import JsonResponse
import os
from django.contrib.auth.models import Permission
from datetime import timedelta
from .forms import EmpleadoForm
import qrcode
from io import BytesIO
import random
import string
import bcrypt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import base64
from cryptography.fernet import Fernet
from PIL import Image, ImageDraw, ImageFont
from cryptography.fernet import Fernet
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from django.db.models import Q, Count
import time
import subprocess
from threading import Timer
import tempfile
import json
from .utils import authenticate_google_drive
import pickle
from googleapiclient.discovery import build
from .models import (
    HojaVida, Foto, Croquis, LuzAgua, Curriculum, Carnet,
    Felcc, Felcn, Rejab, Memorandum, CertificadoExterno, 
    Varios, CertificadoAcademico, Induccion, CartaPresentacion,
    ConveniosContratos, PautasActuacion, ClasificacionFile, FilePersonal
)
 
from django.utils import timezone

 
from django.core.mail import send_mail
 
  
import re
admin_group, created_admin = Group.objects.get_or_create(name='Administradores')
employee_group, created_employee = Group.objects.get_or_create(name='Empleados')

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    permisos_usuario = {modulo['modulo'].nombre: modulo for modulo in modulos_con_permisos}
    tiene_permiso_usuarios = permisos_usuario.get('Usuarios', {}).get('ver', False)
    tiene_permiso_empleados = permisos_usuario.get('Empleados', {}).get('ver', False)
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()
    total_usuarios = User.objects.count()
    total_empleados = DatosPersonal.objects.count()
    resultados = EstadoCertificado.objects.filter(estado__in=[1, 3])
    total_solicitudes = resultados.count()
    total_certificados = CertificadoAprobados.objects.count()
    total_documentos = Foto.objects.count()+  HojaVida.objects.count()+ Croquis.objects.count()+ Memorandum.objects.count()+CartaPresentacion.objects.count()+Varios.objects.count()+Carnet.objects.count() +LuzAgua.objects.count() +Induccion.objects.count() +Curriculum.objects.count()+Felcc.objects.count() +Felcn.objects.count() +Rejab.objects.count() +CertificadoExterno.objects.count() +CertificadoAprobados.objects.count() +CertificadoAcademico.objects.count() +ConveniosContratos.objects.count()+PautasActuacion.objects.count()+Varios.objects.count()
    total_personal = 100   
    perfiles_completos = 43.89  
    porcentaje = (perfiles_completos / total_personal) * 100 if total_personal > 0 else 0
    total_soporte = SolicitudServicioTecnico.objects.filter(estado=False).count()
    request.session['total_soporte'] = total_soporte
    ultimos_soportes = SolicitudServicioTecnico.objects.filter(estado=False).order_by('-id_ticket')[:3]
    
    soportes_info = {}
    
    for i, soporte in enumerate(ultimos_soportes):
        soportes_info[f"soporte_{i+1}_id"]  = soporte.id_ticket  
        soportes_info[f"soporte_{i+1}_mensaje"] = soporte.mensaje  
        soportes_info[f"soporte_{i+1}_nombre"] = soporte.usuario.first_name+' '+soporte.usuario.last_name  
    
    request.session['soportes_info'] = soportes_info
  
    try:
        foto = Foto.objects.filter(file=files.id_file).last() 
        if foto and foto.ruta:
            request.session['foto_url'] = foto.ruta.url
            request.session['grupo_data'] = grupo
        else:
            request.session['foto_url'] = '/media/usuario.png'
            request.session['grupo_data'] = grupo  
    except Exception as e:
        
        request.session['foto_url'] = '/media/usuario.png' 
        request.session['grupo_data'] = grupo
    if foto:
        return render(request, 'dashboard.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo,
        'foto':foto,
        'total_usuarios':total_usuarios,
        'total_documentos':total_documentos,
        'total_certificados':total_certificados,
        'total_empleados':total_empleados,
        'total_solicitudes':total_solicitudes,
        'porcentaje': porcentaje,
        'total_soporte': total_soporte
    })
    else:
        return render(request, 'dashboard.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo,
        'total_usuarios': total_usuarios,
        'total_documentos':total_documentos,
        'total_certificados':total_certificados,
        'total_empleados':total_empleados,
        'total_solicitudes':total_solicitudes,
        'porcentaje': porcentaje,
        'total_soporte': total_soporte
    })
    


def dashboard_empleados(request):
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    permisos_usuario = {modulo['modulo'].nombre: modulo for modulo in modulos_con_permisos}
    tiene_permiso_usuarios = permisos_usuario.get('Usuarios', {}).get('ver', False)
    tiene_permiso_empleados = permisos_usuario.get('Empleados', {}).get('ver', False)
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
  
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()
    foto_persona = '/media/usuario.png'
    if foto:

        drive_url = foto.drive

        
        if '/view' in drive_url:
            file_id = drive_url.split('/d/')[1].split('/')[0]
            foto_persona = f"https://drive.google.com/thumbnail?id={file_id}"
    try:
        foto = Foto.objects.filter(file=files.id_file).last() 
        if foto and foto.ruta:
            request.session['foto'] = foto_persona
            request.session['grupo_data'] = grupo  
        else:
            request.session['foto'] = '/media/usuario.png' 
            request.session['grupo_data'] = grupo   
    except Exception as e:
    
        request.session['foto_url'] = '/media/usuario.png' 
        request.session['grupo_data'] = grupo  
    if foto:
        return render(request, 'dashboard_empleado.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo,
       
        
    })
    else:
        return render(request, 'dashboard_empleado.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo,
        
    })
    

def obtener_permisos_usuario(user):
    permisos_usuario = {}
    modulos = Modulo.objects.all()
    for modulo in modulos:
        permiso = Permiso.objects.filter(empleado=user, modulo=modulo).first()
        if permiso:
            permisos_usuario[modulo.nombre] = {
                'ver': permiso.ver,
                'editar': permiso.editar,
                'eliminar': permiso.eliminar,
            }
        else:
            permisos_usuario[modulo.nombre] = {
                'ver': False,
                'editar': False,
                'eliminar': False,
            }
    return permisos_usuario




def menu(request):
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    permisos_usuario = {modulo['modulo'].nombre: modulo for modulo in modulos_con_permisos}
    tiene_permiso_usuarios = permisos_usuario.get('Usuarios', {}).get('ver', False)
    tiene_permiso_empleados = permisos_usuario.get('Empleados', {}).get('ver', False)
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()
    total_soporte = SolicitudServicioTecnico.objects.filter(estado=False).count()
    
    drive_url = foto.drive

    if '/view' in drive_url:
        file_id = drive_url.split('/d/')[1].split('/')[0]
        foto_persona = f"https://drive.google.com/thumbnail?id={file_id}"
    
    try:
        foto = Foto.objects.filter(file=files.id_file).last() 
        if foto and foto.drive:
            request.session['foto'] = foto_persona
        else:
            request.session['foto'] = '/media/usuario.png'  
    except Exception as e:
     
        request.session['foto'] = '/media/usuario.png' 
    if foto:
        return render(request, 'menu.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo,
        'foto':foto_persona,
        'total_soporte': total_soporte
    })
    else:
        return render(request, 'menu.html', {
        'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados,
        'grupo': grupo ,
        'total_soporte': total_soporte
    })

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')          
            user = authenticate(username=username, password=password)
            return redirect('session')
        else:
            messages.error(request, "La contraseña no es lo suficientemente segura. Debe tener al menos 8 caracteres y contener letras mayúsculas, minúsculas, números y caracteres especiales.")
    else:
        form = UserCreationForm()
    
    return render(request, 'registrar.html', {'form': form})

def agregar_datos_empleado_com(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombres')
            paterno = request.POST.get('paterno')
            materno = request.POST.get('materno')
            correo = request.POST.get('correo')
            ci = request.POST.get('ci')
           
            
            expedido = request.POST.get('expedido')
            fecha_registro = request.POST.get('fecha_registro')
            fecha_objeto = datetime.strptime(fecha_registro, '%Y-%m-%d')
            anio = fecha_objeto.year
            date_joined = timezone.now()
            genero_id = request.POST.get('genero') 
            estado_civil_id = request.POST.get('estado_civil')
            complemento = request.POST.get('complemento')

            if genero_id == 'otro':
                otro_genero = request.POST.get('otro_genero')
                nuevo_genero = Genero(genero=otro_genero)
                nuevo_genero.save()
                genero_id=nuevo_genero.id_genero
            
            if estado_civil_id == 'otro':
                otro_civil = request.POST.get('otro_estado')
                nuevo_estado= EstadoCivil(estado=otro_civil)
                nuevo_estado.save()
                estado_civil_id=nuevo_estado.id_estado
            tipo_sangre = request.POST.get('tipo_sangre') 
            alergias = request.POST.get('alergias')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('autocomplete')
            latitud = request.POST.get('latitud')
            longitud = request.POST.get('longitud')
            departamento_id = request.POST.get('departamento')
            ciudad_id = request.POST.get('ciudad')
            contacto_1 = request.POST.get('contacto_1')
            grado_parentesco_1 = request.POST.get('grado_parentesco_1')
            telefono_1 = request.POST.get('telefono_1')
            contacto_2 = request.POST.get('contacto_2')
            grado_parentesco_2 = request.POST.get('grado_parentesco_2')
            telefono_2 = request.POST.get('telefono_2')
            Hijo1 = request.POST.get('Hijo1')
            usuario = request.POST.get('usuario')

            
            existe_usuario = User.objects.filter(username=usuario).exists()
            existe_ci = DatosPersonal.objects.filter(ci=ci).exists()

            if existe_usuario or existe_ci:
                mensaje = {}
                if existe_usuario:
                    mensaje['usuario'] = 'El usuario que desea registrar ya existe.'
                if existe_ci:
                    mensaje['ci'] = 'La cédula de identidad que desea registrar ya existe.'
                return JsonResponse({'existe': True, 'mensajes': mensaje})

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect(empleados_usuario)
            date_joined = timezone.now()
            new_user = User.objects.create_user(
                username=usuario,
                email=correo,
                password=password1,
                first_name=nombre,
                last_name=paterno+' '+materno,
                date_joined=date_joined
            )
            rol = request.POST.get('rol')
            if rol == '1':
                group, created = Group.objects.get_or_create(name='Administradores')
            elif rol == '2':
                group, created = Group.objects.get_or_create(name='Empleados')
            else:
                messages.error(request, 'Rol no válido')
                return redirect(empleados_usuario)
            new_user.groups.add(group)
            new_user.save()
            modulos = Modulo.objects.filter(grupo=group)
            for modulo in modulos:
                permiso = Permiso.objects.create(
                    empleado=new_user,
                    modulo=modulo,
                    ver=True,
                    agregar=True,
                    editar=True,
                    eliminar=True
                )
                permiso.save()
            dato_id =new_user
            try:
                estado_civil = EstadoCivil.objects.get(id_estado=estado_civil_id)
                genero = Genero.objects.get(id_genero=genero_id)
                departamento = Departamento.objects.get(id_depa = departamento_id)
                ciudad = Ciudad.objects.get(id_ciudad = ciudad_id)
            except (EstadoCivil.DoesNotExist, Genero.DoesNotExist, Sangre.DoesNotExist) as e:
                messages.error(request, f'Error: {str(e)} no válido.')
                return redirect(empleados_usuario)
            foto_puerta = request.FILES['foto_puerta']
            nombre_archivo = f"foto_puertas/{new_user}_{foto_puerta.name}"  
            file_path = default_storage.save(nombre_archivo, foto_puerta) 
            datos_personales = DatosPersonal(
                completo = True,
                empleado_id=new_user,
                nombre=nombre,
                ap_paterno=paterno,
                ap_materno=materno,
                ci=ci,
                complemento = complemento,
                expedido=expedido,
                fecha_nacimiento=fecha_registro,
                genero=genero,  
                estado_civil=estado_civil, 
                tipo_sangre=tipo_sangre, 
                alergias=alergias
            )
            datos_personales.save()
            contato = ContactosPersonal(
                celular=telefono,
                mapa = True,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud,
                hijos= Hijo1,
                empleado_id=new_user,
                ciudad = ciudad,
                departamento = departamento,
                contacto1_nombre=contacto_1,
                contacto1_parentesco=grado_parentesco_1,
                contacto1_numero =telefono_1,
                contacto2_nombre=contacto_2,
                contacto2_parentesco=grado_parentesco_2,
                contacto2_numero =telefono_2,
                foto_puerta = file_path,
            )
            contato.save()
            datos_personales = DatosPersonal.objects.get(empleado_id=dato_id)
            filepersona = FilePersonal(
                empleado_id=datos_personales,
                
            )
            filepersona.save()
        
            return redirect(f"{reverse(empleados_usuario)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(agregar_datos_empleado_com)}?error=true")
 

@login_required
def agregar_empleado(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('nombre')
            last_name = request.POST.get('apellido')
            email = request.POST.get('email')
            username = request.POST.get('usuario')
            password = request.POST.get('password')
            rol = request.POST.get('rol')
            date_joined = timezone.now()

            if User.objects.filter(username=username).exists():
                return JsonResponse({'existe': True})

            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_joined=date_joined
            )

            if rol == '1':
                group, created = Group.objects.get_or_create(name='Administradores')
            elif rol == '2':
                group, created = Group.objects.get_or_create(name='Empleados')
            else:
                messages.error(request, 'Rol no válido')
                return redirect('empleados_usuario')

            new_user.groups.add(group)
            new_user.save()

            datos_personales = DatosPersonal(
                empleado_id=new_user,
                fecha_nacimiento=timezone.now(),
                genero=Genero.objects.first(),
                estado_civil=EstadoCivil.objects.first()
            )
            datos_personales.save()

            contacto = ContactosPersonal(    
                empleado_id=new_user,
                foto_puerta='images_puerta.png'
            )
            contacto.save()

            filepersona = FilePersonal(
                empleado_id=datos_personales,
            )
            filepersona.save()

            modulos = Modulo.objects.filter(grupo=group)
            for modulo in modulos:
                permiso = Permiso.objects.create(
                    empleado=new_user,
                    modulo=modulo,
                    ver=True,
                    agregar=True,
                    editar=True,
                    eliminar=True
                )
                permiso.save()

            return redirect(f"{reverse('empleados')}?success=true")
        

        except Exception as e:
            messages.error(request, 'Ocurrió un error al agregar el empleado.')
            return redirect(f"{reverse('empleados')}?error=true")
  
    return redirect("empleados")

    
def session(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                groups = user.groups.all()
                if groups.exists(): 
                    group_name = groups[0].name 
                    if group_name == 'Administradores':
                        return redirect('dashboard')
                    else:
                   
                        return redirect('dashboard_empleados')
        else:
            messages.error(request, "error")  
    else:
        form = AuthenticationError()
    return render(request, 'login.html', {'form': form})


def certificado_trabajo(request):
    datos = CertificadoAprobados.objects.all().select_related('usuario_modificado')
    usuarios = User.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'certificados_trabajo/certificados.html', {'datos': datos, 'usuarios': usuarios,'grupo':grupo})

def certificado_trabajo_empleados(request):
    datos = CertificadoAprobados.objects.filter(id_dirigido=request.user.id).select_related('usuario_modificado')
    usuarios = User.objects.all()

    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name

    usuario_datos = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario_datos.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()

    return render(request, 'certificados_trabajo/certificados_empleados.html', {'datos': datos, 'usuarios': usuarios, 'grupo':grupo, 'foto':foto})


def solicitud_admi(request):
    datos = EstadoCertificado.objects.all().select_related('solicitud').select_related('usuario_modificado')
    usuarios = User.objects.all().order_by('first_name')
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'certificados_trabajo/solicitud_admi.html', {'datos': datos, 'usuarios':usuarios, 'grupo':grupo})

def obtener_ciudades(request):
    departamento_id = request.GET.get('departamento_id')
    ciudades = Ciudad.objects.filter(departamento_id=departamento_id, activo=True)
   
    ciudad_data = list(ciudades.values('id_ciudad', 'ciudad'))
    return JsonResponse({'ciudades': ciudad_data})

def agregar_datos(request):
    datos = EstadoCertificado.objects.all().select_related('solicitud').select_related('usuario_modificado')
    usuarios = User.objects.all() 
    generos = Genero.objects.all()
    civiles = EstadoCivil.objects.all()
    roles = Group.objects.all()
    departamento = Departamento.objects.all()
    ciudad = Ciudad.objects.all()
    
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'usuarios/agregar_empleado.html', {'datos': datos, 'usuarios':usuarios, 'generos':generos, 'civiles':civiles, 'context':context,'roles':roles,'departamento':departamento,'ciudad':ciudad})

def civil(request):
    datos = EstadoCivil.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/civil.html', {'datos':datos, 'grupo': grupo})

def departamento(request):
    datos= Ciudad.objects.select_related('departamento').all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/departamento.html', {'datos':datos, 'grupo': grupo})

def clasificacion_generacion(request):
    datos= Generacion.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/clasificacion_generacion.html', {'datos':datos, 'grupo': grupo})

def clasificacion_edad(request):
    datos= ClasificacionGrupo.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/clasificacion_edad.html', {'datos':datos, 'grupo': grupo})

def clasificacion_file(request):
    datos= ClasificacionFile.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/clasificacion_file.html', {'datos':datos, 'grupo': grupo})   

def clasificacion_antiguedad(request):
    datos= ClasificacionAnti.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/clasificacion_antiguedad.html', {'datos':datos, 'grupo': grupo})

def genero(request):
    datos= Genero.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/genero.html', {'datos':datos, 'grupo':grupo})




def solicitud_certificado_trabajo(request):
    datos = Certificados.objects.filter(id_dirigido= request.user.id , activo=True).select_related('usuario')
    grupos= request.user.groups.first()
    grupo = grupos.name
    usuarios = User.objects.filter(is_active=True).order_by('first_name')


    usuario_datos = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario_datos.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()

    return render(request, 'certificados_trabajo/solicitudes.html', {'datos': datos, 'usuarios': usuarios, 'grupo':grupo, 'foto':foto})

def reporte_certificado_trabajo(request):
    datos = CertificadoAprobados.objects.all().select_related('usuario_modificado')
    gestiones_unicas = CertificadoAprobados.objects.values('gestion').distinct()
    usuarios = User.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'certificados_trabajo/reportes.html', {'datos': datos, 'usuarios': usuarios, 'gestiones':gestiones_unicas, 'grupo':grupo})


def reporte_certificados(request):
    gestiones = CertificadoAprobados.objects.values('gestion').distinct().order_by('gestion')
  
    if request.method == 'POST':
        gestion = request.POST.get('gestion', None)
        fecha_inicio = request.POST.get('fecha_inicio', None)
        fecha_fin = request.POST.get('fecha_fin', None)
        certificados = CertificadoAprobados.objects.all()
        if gestion and gestion != '0':  
            certificados = certificados.filter(gestion=gestion)

        if fecha_inicio:
            certificados = certificados.filter(fecha_emision__gte=fecha_inicio)

        if fecha_fin:
            certificados = certificados.filter(fecha_emision__lte=fecha_fin)

        datos = certificados
    else:
        datos = CertificadoAprobados.objects.all()

    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuarios = User.objects.all()
    return render(request, 'certificados_trabajo/reportes.html', {'datos': datos, 'usuarios': usuarios, 'gestiones':gestiones,'grupo':grupo})

   


def encargados_usuario(request):
    return render(request, 'usuarios/encargados.html')

def empleados_usuario(request):
    users = User.objects.all() 
    groups = Group.objects.all()
 
    return render(request, 'usuarios/empleados.html', {'users': users, 'groups': groups})
    




def roles_usuario(request):
    permisos = Permission.objects.all()
    roles = Group.objects.prefetch_related('modulo_set').all()
    modulos_por_grupo = [(grupo, grupo.modulo_set.all()) for grupo in roles]
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'usuarios/roles.html', {
        'permisos': permisos,
        'roles': roles,
        'modulos_por_grupo': modulos_por_grupo,
        'grupo':grupo
    })

def permisos(request):
     
    empleados = User.objects.all()
    
    permisos_empleados = {}

    for empleado in empleados:
        permisos = Permiso.objects.filter(empleado=empleado)
        modulos_con_permisos = []
        for permiso in permisos:
            modulos_con_permisos.append({
                'modulo': permiso.modulo,
                'ver': permiso.ver,
                'agregar': permiso.agregar,
                'editar': permiso.editar,
                'eliminar': permiso.eliminar
            })
        permisos_empleados[empleado] = modulos_con_permisos
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name

    grupo_filtrar = Group.objects.get(id=2)
    usuarios_disponibles = grupo_filtrar.user_set.all()
      
    modulos_disponibles = Modulo.objects.filter(grupo=1)
    return render(request, 'usuarios/permisos.html', {
        'permisos_empleados': permisos_empleados,
        'grupo': grupo,
        'usuarios_disponibles': usuarios_disponibles,
        'modulos_disponibles': modulos_disponibles
            
    })

def reporte_usuario(request):
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'usuarios/reportes.html',{'grupo':grupo})

def agregar_solicitud(request):
    datos = Certificados.objects.all()
    if request.method == "POST":
        if request.POST.get("dirigido") and request.POST.get("gestion") and request.POST.get("fecha_registro") and request.POST.get("email") and request.POST.get("referencia") and request.POST.get("usuario"):
            certificado = Certificados()
            fecha_actual = timezone.now()
            certificado.fecha_solicitud = request.POST.get("fecha_registro")
            certificado.fecha_registro = fecha_actual
            certificado.fecha_modificado = fecha_actual
            certificado.correo = request.POST.get("email")
            certificado.requerimiento = request.POST.get("requerimiento")
            id_dirigido = request.POST.get("dirigido")
            user_dirigido = get_object_or_404(User, id=id_dirigido)
            certificado.dirigido = user_dirigido.first_name+' '+user_dirigido.last_name
            certificado.gestion = request.POST.get("gestion")
            certificado.tipo = request.POST.get("referencia")
            certificado.estado = 1
            id_usuario = request.POST.get('id_usuario')
            usuario = User.objects.get(id=id_usuario)
            certificado.usuario = usuario
            certificado.id_dirigido = id_usuario
            certificado.save()

            ultimo_estado = EstadoCertificado.objects.last()
            if ultimo_estado:
                correlativo_nuevo = ultimo_estado.correlativo + 1
            else:
                correlativo_nuevo = 1

            estado = EstadoCertificado()
            estado.solicitud = certificado  
            estado.correlativo = correlativo_nuevo
            estado.estado = 1
            estado.usuario_modificado = usuario
            estado.observacion = 'Sin Observaciones'
            estado.save()
            mensaje = 1
            datos = Certificados.objects.filter(usuario=request.user).select_related('usuario')
            datos_invertidos = list(datos)[::-1]  
            usuarios = User.objects.all()
            grupos = request.user.groups.first()
            grupo= grupos.name
            return render(request, 'certificados_trabajo/solicitudes.html', {'datos': datos_invertidos, 'usuarios': usuarios, 'mensaje':mensaje, 'grupo' :grupo})

        else:
            mensaje = 2
            return render(request, 'certificados_trabajo/solicitudes.html', {'datos': datos, 'mensaje':mensaje})


def agregar_solicitud_2(request):
    datos = Certificados.objects.all()
    if request.method == "POST":
        if request.POST.get("dirigido") and request.POST.get("gestion") and request.POST.get("fecha_registro") and request.POST.get("email") and request.POST.get("referencia") and request.POST.get("usuario"):
            certificado = Certificados()
            fecha_actual = timezone.now()
            certificado.fecha_solicitud = request.POST.get("fecha_registro")
            certificado.fecha_registro = fecha_actual
            certificado.fecha_modificado = fecha_actual
            certificado.correo = request.POST.get("email")
            id_dirigido = request.POST.get("dirigido")
            user_dirigido = get_object_or_404(User, id=id_dirigido)
            certificado.dirigido = user_dirigido.first_name+' '+user_dirigido.last_name
            certificado.gestion = request.POST.get("gestion")
            certificado.tipo = request.POST.get("referencia")
            certificado.estado = 1
            id_usuario = request.POST.get('id_usuario')
            usuario = User.objects.get(id=id_usuario)
            certificado.usuario = usuario
            certificado.id_dirigido = id_dirigido
            certificado.save()

            ultimo_estado = EstadoCertificado.objects.last()
            if ultimo_estado:
                correlativo_nuevo = ultimo_estado.correlativo + 1
            else:
                correlativo_nuevo = 1


            estado = EstadoCertificado()
            estado.solicitud = certificado  
            estado.correlativo = correlativo_nuevo
            estado.estado = 1
            estado.usuario_modificado = usuario
            estado.observacion = 'Sin Observaciones'
            estado.save()
            mensaje = 1
            return redirect('solicitud_admi')
        else:
            messages.error(request, "Hubo un error al agregar el registro.")
            mensaje = 2
            return render(request, 'certificados_trabajo/solicitud_admi.html', {'datos': datos, 'mensaje': mensaje})

def cambiar_estado(request):
    if request.method == 'POST':
        id_estado = request.POST.get('id_estado')
        id_solicitud = request.POST.get('id_solicitud')
        emitido = request.POST.get('emitido')
        certificado_obtenido = get_object_or_404(Certificados, id_certificado=id_solicitud)
        estado_obtenido = get_object_or_404(EstadoCertificado, id_estado=id_estado)
        aprobado = request.POST.get('estado')
        estado_obtenido.estado = aprobado
        certificado_obtenido.estado = aprobado
        observaciones = request.POST.get('observacion')
        if observaciones == '':
            estado_obtenido.observacion = 'Sin Observaciones'
        else:
            estado_obtenido.observacion = observaciones
        
        estado_obtenido.save()
        certificado_obtenido.save()
        anio = certificado_obtenido.gestion
        ultimo_estado = CertificadoAprobados.objects.filter(gestion=anio).order_by('-id_certificado_a').first()

        if ultimo_estado:
            if ultimo_estado.codigo != 'ANULADO':
           
                correlativo_nuevo = ultimo_estado.correlativo + 1
            else:
                correlativo_nuevo = ultimo_estado.correlativo
                
        else:
            correlativo_nuevo = 1
            
        aprobado = int(aprobado)
        if aprobado==2:
            nuevo_certificado = CertificadoAprobados()
            nuevo_certificado.correlativo = correlativo_nuevo
            nuevo_certificado.dirigido = certificado_obtenido.dirigido
            nuevo_certificado.emitido = emitido
            nuevo_certificado.id_dirigido = certificado_obtenido.id_dirigido
            nuevo_certificado.solicitud = certificado_obtenido
            nuevo_certificado.correo = certificado_obtenido.correo
            nuevo_certificado.referencia = certificado_obtenido.tipo
            nuevo_certificado.estado = 1
            nuevo_certificado.gestion = certificado_obtenido.gestion
            id_usuario = request.POST.get('id_usuario')
            usuario = User.objects.get(id=id_usuario)
            usuario_certificado = DatosPersonal.objects.get(empleado_id=certificado_obtenido.id_dirigido)
            file = FilePersonal.objects.get(empleado_id=usuario_certificado.id_datos)
            nuevo_certificado.file = file
            nuevo_certificado.usuario_modificado = usuario
            nuevo_certificado.codigo = 'VLSCSA/CDT/' + str(correlativo_nuevo).zfill(3) + '-' + str(certificado_obtenido.gestion)
            nuevo_certificado.save()
            return redirect('certificado')
        
        return redirect('certificado')
    else:
        return redirect('solicitud_admi')
    
def listar_certificado(request):
    datos = Certificados.objects.all()
    return render(request, 'certificados_trabajo/solicitud_admi.html', {'datos': datos})

def listar_certificado_empleados(request):
    datos = Certificados.objects.filter(dirigido=request.user)
    grupos = request.user.groups.first()
    grupo =grupos.name
    return render(request, 'certificados_trabajo/solicitud_admi.html', {'datos': datos, 'grupos':grupo})

def cierre_gestion(request):
    gestiones_conteo = CertificadoAprobados.objects.values('gestion').annotate(abiertos=Count('id_certificado_a', filter=Q(cierre=True)),  
                  cerrados=Count('id_certificado_a', filter=Q(cierre=False))) 

    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'certificados_trabajo/cierre_gestion.html', {'gestiones': gestiones_conteo, 'grupo':grupo})

def cerrar_certificados(request):
    if request.method == 'POST':
        gestion = request.POST.get('gestion')  
        if gestion:  
            CertificadoAprobados.objects.filter(gestion=gestion).update(cierre=False)
        return redirect(cierre_gestion)  
    else:
        
        return render(request, 'certificados_trabajo/cerrar_certificados.html')

def abrir_certificados(request):
    if request.method == 'POST':
        gestion = request.POST.get('gestion') 
        if gestion:  
            CertificadoAprobados.objects.filter(gestion=gestion).update(cierre=True)
        return redirect(cierre_gestion)  
    else:
        
        return render(request, 'certificados_trabajo/cerrar_certificados.html')


def agregar_documentos_file(request):
    if request.method == 'POST':
        try:
            file_req = request.POST.get('documento-id')
            empleado_nombre = FilePersonal.objects.get(id_file = file_req)
            dato_nombre_empleado = empleado_nombre.empleado_id.empleado_id.first_name + ' ' + empleado_nombre.empleado_id.empleado_id.last_name
           
            fecha_actual = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
            service = authenticate_google_drive()

            def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
                query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
                if carpeta_padre_id:
                    query += f" and '{carpeta_padre_id}' in parents"
                resultados = service.files().list(q=query, fields="files(id, name)").execute()
                folders = resultados.get('files', [])

                if folders:
                    return folders[0]['id']
                else:
                    file_metadata = {
                        'name': carpeta_nombre,
                        'mimeType': 'application/vnd.google-apps.folder',
                    }
                    if carpeta_padre_id:
                        file_metadata['parents'] = [carpeta_padre_id]
                    
                    carpeta = service.files().create(body=file_metadata, fields='id').execute()
              
                    return carpeta['id']

            carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA FILE VILASECA')
            carpeta_empleado_id = obtener_o_crear_carpeta(dato_nombre_empleado, carpeta_padre_id=carpeta_documentos_id)

            def guardar_documento(modelo, archivo_nombre, archivo, clasificacion):
                extension = archivo.name.split('.')[-1]
                archivo_guardado_nombre = f"{archivo_nombre}_{fecha_actual}.{extension}"
                temp_file_path = os.path.join(archivo_guardado_nombre)
                with open(temp_file_path, 'wb') as f:
                    for chunk in archivo.chunks():
                        f.write(chunk)
                file_metadata = {
                    'name': archivo_guardado_nombre,
                    'parents': [carpeta_empleado_id] 
                }
                media = MediaFileUpload(temp_file_path, mimetype=archivo.content_type)
                file_drive = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()

              
                try:
                    file_personal = FilePersonal.objects.get(id_file=file_req)
                except FilePersonal.DoesNotExist:
                    print(f"[ERROR] No se encontró un FilePersonal con ID {file_req}")
                    file_personal = None

                ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"

                # ruta_final = f"https://drive.google.com/uc?id={file_drive['id']}"

                # ruta_final = f"https://drive.google.com/thumbnail?id={file_drive['id']}"
              
                
                if file_personal:
                    modelo.objects.create(
                        file=file_personal,
                        ruta=ruta_final,
                        drive=ruta_final,
                        fecha_registro=timezone.now(),
                        clasificacion=clasificacion
                    )
                    print(f"[DEBUG] Documento de {archivo_nombre} creado en la base de datos.")
                else:
                    print(f"[ERROR] No se pudo crear el documento para {archivo_nombre}, ya que no se encontró el FilePersonal.")
                def eliminar_archivo():
                    try:
                        os.remove(temp_file_path)
                        print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                    except Exception as e:
                        print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")
                Timer(300, eliminar_archivo).start()  

            archivos_y_clasificaciones = [
                ('hojaDeVida', 'HDV-002', HojaVida),
                ('foto', 'FOTO', Foto),
                ('croquisDomicilio', 'CD', Croquis),
                ('facturaLuzAgua', 'FACT', LuzAgua),
                ('curriculum', 'CV', Curriculum),
                ('carnetIdentidad', 'CI', Carnet),
                ('certificadoFELCC', 'FELCC', Felcc),
                ('certificadoFELCN', 'FELCN', Felcn),
                ('certificadoREJAP', 'REJAP', Rejab),
                ('memorandums', 'MEMO', Memorandum),
                ('certificadosTrabajo', 'CT', CertificadoExterno),
                ('documentosVarios', 'DV', Varios),
                ('certificadosAcademicos', 'CA', CertificadoAcademico),
                ('listaVerificacionInduccion', 'LVIP-005', Induccion),
                ('cartaPresentacion', 'CPE-001', CartaPresentacion),
                ('contratosConvenios', 'CON-PER', ConveniosContratos),
                ('pautasActuacionProfesional', 'PAP-001', PautasActuacion)
            ]

            for campo, clasificacion_siglas, modelo in archivos_y_clasificaciones:
                if campo in request.FILES:
                    archivos = request.FILES.getlist(campo) 
                    clasificacion = ClasificacionFile.objects.get(siglas=clasificacion_siglas)
                    for archivo in archivos:
                        print(f"[DEBUG] Archivo {campo} recibido: {archivo.name}")
                        guardar_documento(modelo, campo, archivo, clasificacion)

            grupos_usuario = request.user.groups.first()
            grupo = grupos_usuario.name
            if grupo == 'Administradores':
              
                return redirect(f"{reverse(documento)}?success=true")
            else:
               
                return redirect(f"{reverse(documento_empleados)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(documento)}?error=true")
  
     



def cargar_documento(request):
    def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
        query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
        if carpeta_padre_id:
            query += f" and '{carpeta_padre_id}' in parents"
        resultados = service.files().list(q=query, fields="files(id, name)").execute()
        folders = resultados.get('files', [])

        if folders:
            return folders[0]['id']
        else:
            file_metadata = {
                'name': carpeta_nombre,
                'mimeType': 'application/vnd.google-apps.folder',
            }
            if carpeta_padre_id:
                file_metadata['parents'] = [carpeta_padre_id]

            carpeta = service.files().create(body=file_metadata, fields='id').execute()
            print(f"[DEBUG] Carpeta '{carpeta_nombre}' creada con ID: {carpeta['id']}")
            return carpeta['id']
    if request.method == 'POST' and request.FILES.get('adjunto'):
        certificado = request.POST.get('id_certificado')
        confirmar = request.POST.get('enviar')
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if confirmar == 'on':
            certificado_obtenido = get_object_or_404(CertificadoAprobados, id_certificado_a=certificado)
            documento = request.FILES['adjunto']
            service = authenticate_google_drive()

           

            carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA FILE VILASECA')
            carpeta_empleado_id = obtener_o_crear_carpeta('CERTIFICADOS TRABAJO', carpeta_padre_id=carpeta_documentos_id)
            nombre_certificado =certificado_obtenido.dirigido
 
            archivo_guardado_nombre = f"{nombre_certificado}_{fecha_actual}"
            temp_file_path = os.path.join(settings.MEDIA_ROOT, archivo_guardado_nombre) 

            with open(temp_file_path, 'wb') as f:
                for chunk in documento.chunks():
                    f.write(chunk)

            file_metadata = {
                'name': archivo_guardado_nombre,
                'parents': [carpeta_empleado_id]
            }
            media = MediaFileUpload(temp_file_path, mimetype=documento.content_type)
            file_drive = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f"[DEBUG] Archivo subido a Google Drive con ID: {file_drive['id']}")
            ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"

            def eliminar_archivo():
                try:
                    os.remove(temp_file_path)
                    print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")

            Timer(300, eliminar_archivo).start()

            certificado_obtenido.drive = ruta_final
            certificado_obtenido.adjunto = ruta_final
            certificado_obtenido.save()

            email = certificado_obtenido.correo
            subject = f"Certificado de Trabajo - {certificado_obtenido.codigo}"
            message = f"Estimado usuario,\n\nAdjunto el certificado de trabajo con el código: {certificado_obtenido.codigo}.\n\nSaludos."

            email_message = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            with open(temp_file_path, 'rb') as f:
                email_message.attach(documento.name, f.read(), documento.content_type)

            email_message.send()
            return redirect('certificado')

        else:
            certificado_obtenido = get_object_or_404(CertificadoAprobados, id_certificado_a=certificado)
            documento = request.FILES['adjunto']
            service = authenticate_google_drive()

            carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA FILE VILASECA')
            carpeta_empleado_id = obtener_o_crear_carpeta('CERTIFICADOS TRABAJO', carpeta_padre_id=carpeta_documentos_id)

            nombre_certificado =certificado_obtenido.dirigido
 
            archivo_guardado_nombre = f"{nombre_certificado}_{fecha_actual}"
            temp_file_path = os.path.join(settings.MEDIA_ROOT, archivo_guardado_nombre)
            with open(temp_file_path, 'wb') as f:
                for chunk in documento.chunks():
                    f.write(chunk)

            file_metadata = {
                'name': archivo_guardado_nombre,
                'parents': [carpeta_empleado_id]
            }
            media = MediaFileUpload(temp_file_path, mimetype=documento.content_type)
            file_drive = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f"[DEBUG] Archivo subido a Google Drive con ID: {file_drive['id']}")
            ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"

            def eliminar_archivo():
                try:
                    os.remove(temp_file_path)
                    print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")

            Timer(300, eliminar_archivo).start()

            certificado_obtenido.drive = ruta_final
            certificado_obtenido.adjunto = ruta_final
            certificado_obtenido.save()

            return redirect('certificado')

    datos = CertificadoAprobados.objects.all()
    return render(request, 'certificados_trabajo/certificados.html', {'datos': datos})






def editar_solicitud(request):
    if request.method == 'POST':
       id = request.POST.get('id_certificado_editar')
       certificado = get_object_or_404(Certificados, id_certificado=id)
       certificado.dirigido = request.POST.get('dirigido_editar')
       certificado.emitido = request.POST.get('emitido_editar')
       if request.POST.get('fecha_registro_editar') !='':
            certificado.fecha_solicitud =request.POST.get('fecha_registro_editar')
       certificado.fecha_modificado = timezone.now()
       certificado.correo = request.POST.get('correo_editar')
       id_usuario = request.POST.get('id_usuario')
       certificado.gestion = request.POST.get('gestion_editar')
       usuario = User.objects.get(id=id_usuario)
       certificado.usuario = usuario
       certificado.tipo = request.POST.get('referencia_editar')
       certificado.requerimiento = request.POST.get('requerimiento_editar')
       certificado.save()
    
    datos = Certificados.objects.all()
    return redirect('solicitud')



def editar_solicitud2(request):
    if request.method == 'POST':
       id = request.POST.get('id_certificado')
       certificado = get_object_or_404(Certificados, id_certificado=id)
       certificado.dirigido = request.POST.get('dirigido')
       certificado.gestion = request.POST.get('gestion')
       if request.POST.get('fecha_registro') !='':
            certificado.fecha_solicitud =request.POST.get('fecha_registro')
       certificado.fecha_modificado = now().strftime('%Y-%m-%d')  
       certificado.correo = request.POST.get('email')
       id_usuario = request.POST.get('id_usuario')
       usuario = User.objects.get(id=id_usuario)
       certificado.usuario = usuario
       certificado.tipo = request.POST.get('referencia')
       certificado.requerimiento = request.POST.get('requerimiento_editar')
       certificado.save()
    
    datos = Certificados.objects.all()
    return redirect('solicitud_admi')


def eliminar_solicitud(request):
    if request.method == 'POST':
        id = request.POST.get('id_certificado')
        certificado = get_object_or_404(Certificados, id_certificado=id)
        if certificado.activo == True:
            certificado.activo = False
        else:
            certificado.activo = True

        certificado.save()
        return redirect('solicitud') 
    else:
        datos = Certificados.objects.all()
        return render(request, 'certificados_trabajo/solicitudes.html', {'datos': datos})
    

def eliminar_solicitud_adm(request):
    if request.method == 'POST':
        id = request.POST.get('id_certificado')
        id=int(id)
        certificado = get_object_or_404(Certificados, id_certificado=id)
        if certificado.activo == True:
            certificado.activo = False
        else:
            certificado.activo = True

        certificado.save()
        return redirect('solicitud_admi') 
    else:
        datos = Certificados.objects.all()
        return render(request, 'certificados_trabajo/solicitudes_admin.html', {'datos': datos})
    

def eliminar_certificado(request):
    if request.method == 'POST':
        id = request.POST.get('id_certificado')
        certificado = get_object_or_404(CertificadoAprobados, id_certificado_a=id)
        if certificado.activo == True:
            certificado.activo = False
            certificado.codigo = 'ANULADO'
            certificado.drive = 'ANULADO'

        certificado.save()
        return redirect('certificado') 
    else:
        datos = CertificadoAprobados.objects.all()
        return render(request, 'certificados_trabajo/certificados.html', {'datos': datos})
    

def nuevo_certificado(request):
    if request.method == 'POST':
        anio = request.POST.get('gestion')
        ultimo_estado = CertificadoAprobados.objects.filter(gestion=anio).order_by('-id_certificado_a').first()
        if ultimo_estado:
            if ultimo_estado.codigo != 'ANULADO':
                correlativo_nuevo = ultimo_estado.correlativo + 1
            else:
                correlativo_nuevo = ultimo_estado.correlativo
        else:
            correlativo_nuevo = 1
            
        
        nuevo_certificado = CertificadoAprobados()
        nuevo_certificado.correlativo = correlativo_nuevo
        id_dirigido = request.POST.get("dirigido")
        user_dirigido = get_object_or_404(User, id=id_dirigido)
        nuevo_certificado.dirigido = user_dirigido.first_name+' '+user_dirigido.last_name
        nuevo_certificado.emitido =  request.POST.get('emitido')
        nuevo_certificado.referencia =  request.POST.get('referencia')
        nuevo_certificado.correo = request.POST.get('email')
        nuevo_certificado.fecha_emision =  request.POST.get('fecha_registro')
        nuevo_certificado.estado =  2
        nuevo_certificado.id_dirigido = id_dirigido
        fecha_actual = timezone.now()
        gestion_actual = fecha_actual.year
        nuevo_certificado.gestion =  request.POST.get('gestion')
        id_usuario = request.POST.get('id_usuario')
        usuario = User.objects.get(id=id_usuario)
        datosEmpleado= DatosPersonal.objects.get(empleado_id = id_dirigido)
        file = FilePersonal.objects.get(empleado_id=datosEmpleado.id_datos)
        nuevo_certificado.file = file
        nuevo_certificado.usuario_modificado = usuario
        nuevo_certificado.codigo = 'VLSCSA/CDT/' + str(correlativo_nuevo).zfill(3) + '-' + str(anio)
        nuevo_certificado.save()
    datos = CertificadoAprobados.objects.all()
    messages.success(request, 'Datos del Nuevo Certificado han sido registrados exitosamente.')
    return redirect('certificado')

def editar_certificado(request):
    if request.method == 'POST':
       id = request.POST.get('id_certificado')
       certificado = get_object_or_404(CertificadoAprobados, id_certificado_a=id)
       certificado.dirigido = request.POST.get('dirigido')
       certificado.emitido = request.POST.get('emitido')
       certificado.fecha_emision = timezone.now()
       certificado.correo = request.POST.get('email')
       id_usuario = request.POST.get('id_usuario')
       certificado.gestion = request.POST.get('gestion')
       usuario = User.objects.get(id=id_usuario)
       certificado.usuario_modificado = usuario
       certificado.referencia = request.POST.get('referencia')
       certificado.save()
    
    return redirect('certificado')

def error_404(request, exception):
    return render(request, '404.html', {}, status=404)

def error_500(request):
    return render(request, '500.html', {}, status=500)

def error_403(request, exception):
    return render(request, '403.html', {}, status=403)

def obtener_certificado(request, certificado_id):
    try:
        certificado = Certificados.objects.get(id_certificado=certificado_id)
        data = {
            'id_certificado': certificado.id_certificado,
            'dirigido': certificado.dirigido,
            'correo': certificado.correo,
            'fecha_solicitud': certificado.fecha_solicitud.strftime('%Y-%m-%d'),
            'gestion': certificado.gestion,
            'tipo': certificado.tipo,
            'requerimiento': certificado.requerimiento,
        }
       
        return JsonResponse(data)
    except Certificados.DoesNotExist:
        return JsonResponse({'error': 'Certificado no encontrado'}, status=404)
    

def obtener_datos(request, datos_id):
    try:
        empleado = DatosPersonal.objects.get(id_datos=datos_id)
        data = {
            'id_datos': empleado.id_datos,
            'ci': empleado.ci,
            'expedido': empleado.expedido,
            'nombre': empleado.nombre,
            'ap_paterno': empleado.ap_paterno,
            'ap_materno': empleado.ap_materno,
            'fecha_nacimiento': empleado.fecha_nacimiento.strftime('%Y-%m-%d'),
            'genero':empleado.genero.id_genero,
            'estado_civil': empleado.estado_civil.id_estado,
            'sangre': empleado.tipo_sangre,
            'alergias': empleado.alergias,
            'correo': empleado.empleado_id.email
        }
      
        return JsonResponse(data)
    except DatosPersonal.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    


def obtener_datos_contacto(request, datos_id):
    try:
        empleado = DatosPersonal.objects.get(id_datos=datos_id)
        data = {
        }
        return JsonResponse(data)
    except DatosPersonal.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def datos_contratos(request):
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuarios = User.objects.filter(is_active = True)
    tipos_contrato = TipoContrato.objects.all()
    tipos_registro = TipoRegistro.objects.all()
    datos_empleado = Empleo.objects.all()
    cargos = AreasCargos.objects.filter(activo = True)
    oficinas = Oficina.objects.filter(activo = True)
 
    return render(request, 'empleados/datos_contrato.html',{'grupo':grupo, 'datos_empleado': datos_empleado,'tipos_contrato':tipos_contrato, 'tipos_registro': tipos_registro, 'usuarios': usuarios, 'cargos': cargos , 'oficinas':oficinas})


def datos_contratos_empleados(request):
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'empleados/datos_contrato.html',{'grupo':grupo})   

def agregar_nuevo_empleado(request):
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    modulo_empleados = next((m for m in modulos_con_permisos if m['modulo'].nombre == "Empleados"), None)
   
    if not modulo_empleados or not modulo_empleados['agregar']:
        return render(request, 'menu.html')
    
    datos = EstadoCertificado.objects.all().select_related('solicitud').select_related('usuario_modificado')
    usuarios = User.objects.all() 
    generos = Genero.objects.all()
    civiles = EstadoCivil.objects.all()
    roles = Group.objects.all()
    departamento = Departamento.objects.all()
    ciudad = Ciudad.objects.all()
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    grupos = request.user.groups.first()
    grupo = grupos.name
    return render(request, 'empleados/agregar_nuevo_empleado.html', {'datos': datos, 'usuarios':usuarios, 'generos':generos, 'civiles':civiles, 'context':context,'roles':roles,'departamento':departamento,'ciudad':ciudad, 'grupo': grupo})



def obtener_modulos_con_permisos(usuario):
    grupos = usuario.groups.all()
    modulos_accesibles = Modulo.objects.filter(grupo__in=grupos, activo=True)
    modulos_con_permisos = []
    for modulo in modulos_accesibles:
        permiso = Permiso.objects.filter(empleado=usuario, modulo=modulo).first()
        if permiso:
            modulos_con_permisos.append({
                'modulo': modulo,
                'ver': permiso.ver,
                'agregar': permiso.agregar,
                'editar': permiso.editar,
                'eliminar': permiso.eliminar
            })

    return modulos_con_permisos


def lista_empleados(request):
    # modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    # print(modulos_con_permisos)
    # modulo_empleados = next((m for m in modulos_con_permisos if m['modulo'].nombre == "Empleados"), None)
   
    # if not modulo_empleados or not modulo_empleados['ver']:
    #     return render(request, 'menu.html')

    datos = DatosPersonal.objects.all().select_related(
        'genero', 'estado_civil', 'empleado_id'
    )
    empleados_info = []
    fecha_actual = timezone.now().date()

    for empleado in datos:
        fecha_nacimiento = empleado.fecha_nacimiento
        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        clasificacion_grupo = ClasificacionGrupo.objects.filter(
            rango_inicio__lte=edad, rango_fin__gte=edad, activo=True
        ).first()
        clasificacion_grupo_text = clasificacion_grupo.clasificacion if clasificacion_grupo else 'Sin clasificación'
        año_nacimiento = fecha_nacimiento.year
        generacion = Generacion.objects.filter(
            rango_inicio__lte=año_nacimiento, rango_fin__gte=año_nacimiento, activo=True
        ).first()
        generacion_text = generacion.generacion if generacion else 'Sin generación'
        empleados_info.append({
            'empleado': empleado,
            'edad': edad,
            'clasificacion_grupo': clasificacion_grupo_text,
            'generacion': generacion_text
        })
    
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    permisos_usuario = {modulo['modulo'].nombre: modulo for modulo in modulos_con_permisos}
     
    tiene_permiso_usuarios = permisos_usuario.get('Usuarios', {}).get('ver', False)
    tiene_permiso_empleados = permisos_usuario.get('Empleados', {}).get('ver', False)
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
     
    usuarios = User.objects.all() 
    generos = Genero.objects.all()
    civiles = EstadoCivil.objects.all()
    roles = Group.objects.all()
    departamento = Departamento.objects.all()
    ciudad = Ciudad.objects.all()
 
    return render(request, 'empleados/lista_empleados.html', {'empleados_info': empleados_info, 'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados, 'grupo': grupo, 'generos':generos, 'civiles':civiles})

def lista_maestra(request):
    # Obtener los módulos y permisos del usuario
    # modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    # print(modulos_con_permisos)
    # modulo_empleados = next((m for m in modulos_con_permisos if m['modulo'].nombre == "Empleados"), None)
    # if not modulo_empleados or not modulo_empleados['ver']:
    #     return render(request, 'menu.html')
    datos = DatosPersonal.objects.filter(empleado_id=request.user).select_related( 
        'genero', 'estado_civil', 'empleado_id'
    )
    empleados_info = []
    fecha_actual = timezone.now().date()

    for empleado in datos:
        fecha_nacimiento = empleado.fecha_nacimiento
        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        clasificacion_grupo = ClasificacionGrupo.objects.filter(
            rango_inicio__lte=edad, rango_fin__gte=edad, activo=True
        ).first()
        clasificacion_grupo_text = clasificacion_grupo.clasificacion if clasificacion_grupo else 'Sin clasificación'
        año_nacimiento = fecha_nacimiento.year
        generacion = Generacion.objects.filter(
            rango_inicio__lte=año_nacimiento, rango_fin__gte=año_nacimiento, activo=True
        ).first()
        generacion_text = generacion.generacion if generacion else 'Sin generación'
        usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
        usuario_file=usuario.id_datos
        files = FilePersonal.objects.get(empleado_id=usuario_file) 
        generos =  Genero.objects.all()
        civiles = EstadoCivil.objects.all()
        foto = Foto.objects.filter(file=files.id_file).last()
        empleados_info.append({
            'empleado': empleado,
            'edad': edad,
            'clasificacion_grupo': clasificacion_grupo_text,
            'generacion': generacion_text,
            'foto':foto,
            'generos' :  generos,
            'civiles' : civiles,
           

        })
    
    modulos_con_permisos = obtener_modulos_con_permisos(request.user)
    permisos_usuario = {modulo['modulo'].nombre: modulo for modulo in modulos_con_permisos}
     
    tiene_permiso_usuarios = permisos_usuario.get('Usuarios', {}).get('ver', False)
    tiene_permiso_empleados = permisos_usuario.get('Empleados', {}).get('ver', False)
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
     
    return render(request, 'empleados/lista_maestra.html', {'empleados_info': empleados_info, 'tiene_permiso_usuarios': tiene_permiso_usuarios,
        'tiene_permiso_empleados': tiene_permiso_empleados, 'grupo': grupo,'foto':foto, 'generos' :  generos,
            'civiles' : civiles,})

def personal_actual(request):
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    departamento = Departamento.objects.all()
    ciudad = Ciudad.objects.all()
    datos = ContactosPersonal.objects.all().select_related(
         'empleado_id','departamento','ciudad'
    )
    return render(request, 'empleados/personal_actual.html', {'datos':datos, 'grupo': grupo, 'departamento': departamento, 'ciudad':ciudad})


def personal_actual_empleado(request):
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=files.id_file).last()
    departamento = Departamento.objects.all()
    ciudad = Ciudad.objects.all()
    datos = ContactosPersonal.objects.filter(empleado_id=request.user).select_related(
         'empleado_id','departamento','ciudad'
    )
    return render(request, 'empleados/personal_actual_empleado.html', {'datos':datos, 'grupo': grupo, 'foto':foto, 'departamento': departamento, 'ciudad':ciudad})





def estadisticas(request):
    datos = DatosPersonal.objects.all().select_related(
        'genero', 'estado_civil', 'empleado_id'
    )
    generos = Genero.objects.all()
    genero_labels = []
    genero_counts = []
    for sugenero in generos:
        generos_empleados = DatosPersonal.objects.filter(genero=sugenero).count()
        genero_labels.append(sugenero.genero) 
        genero_counts.append(generos_empleados)
    generacion_labels = []
    generacion_counts = []
    clasificacion_grupo_labels = []
    clasificacion_grupo_counts = []
    fecha_actual = timezone.now().date()
    empleados_info = []
    for empleado in datos:
        fecha_nacimiento = empleado.fecha_nacimiento
        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        clasificacion_grupo = ClasificacionGrupo.objects.filter(
            rango_inicio__lte=edad, rango_fin__gte=edad, activo=True
        ).first()
        clasificacion_grupo_text = clasificacion_grupo.clasificacion if clasificacion_grupo else 'Sin clasificación'
        año_nacimiento = fecha_nacimiento.year
        generacion = Generacion.objects.filter(
            rango_inicio__lte=año_nacimiento, rango_fin__gte=año_nacimiento, activo=True
        ).first()
        generacion_text = generacion.generacion if generacion else 'Sin generación'
        empleados_info.append({
            'empleado': empleado,
            'edad': edad,
            'clasificacion_grupo': clasificacion_grupo_text,
            'generacion': generacion_text
        })
        if generacion_text not in generacion_labels:
            generacion_labels.append(generacion_text)
            generacion_counts.append(1)
        else:
            idx = generacion_labels.index(generacion_text)
            generacion_counts[idx] += 1
        if clasificacion_grupo_text not in clasificacion_grupo_labels:
            clasificacion_grupo_labels.append(clasificacion_grupo_text)
            clasificacion_grupo_counts.append(1)
        else:
            idx = clasificacion_grupo_labels.index(clasificacion_grupo_text)
            clasificacion_grupo_counts[idx] += 1

    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'empleados/estadisticas.html', {
        'empleados_info': empleados_info,
        'generacion_labels': generacion_labels,
        'generacion_counts': generacion_counts,
        'clasificacion_grupo_labels': clasificacion_grupo_labels,
        'clasificacion_grupo_counts': clasificacion_grupo_counts,
        'genero_labels': genero_labels,
        'genero_counts': genero_counts,
        'grupo':grupo
    })


def mapa_empleados(request):
    contactos = ContactosPersonal.objects.filter(mapa = True)
    empleados_data = []
    for contacto in contactos:
        if contacto.empleado_id:  
            empleado_nombre = contacto.empleado_id.first_name + " " + contacto.empleado_id.last_name
        else:
            empleado_nombre = "Nombre no disponible"
        if contacto.latitud and contacto.longitud:
            empleados_data.append({
                "lat": contacto.latitud,
                "lon": contacto.longitud,
                "nombre": empleado_nombre,
                "direccion": contacto.direccion,
            })
        else:
            print(f"Empleado sin coordenadas: {empleado_nombre}")
    
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
  
    return render(request, 'empleados/mapa_empleados.html', {
        'empleados': empleados_data,
        'grupo': grupo
    })

def documento(request):
    personas = DatosPersonal.objects.all()
    files = []
    for persona in personas:
        file_personal = FilePersonal.objects.filter(empleado_id=persona).first()
        if file_personal:
            documentos = {
                'id': file_personal.id_file,
                'foto': Foto.objects.filter(file=file_personal).count(),
                'hoja_vida': HojaVida.objects.filter(file=file_personal).count(),
                'croquis': Croquis.objects.filter(file=file_personal).count(),
                'memorandum': Memorandum.objects.filter(file=file_personal).count(),
                'carta_presentacion': CartaPresentacion.objects.filter(file=file_personal).count(),
                'varios': Varios.objects.filter(file=file_personal).count(),
                'carnet': Carnet.objects.filter(file=file_personal).count(),
                'luz_agua': LuzAgua.objects.filter(file=file_personal).count(),
                'induccion': Induccion.objects.filter(file=file_personal).count(),
                'curriculum': Curriculum.objects.filter(file=file_personal).count(),
                'felcc': Felcc.objects.filter(file=file_personal).count(),
                'felcn': Felcn.objects.filter(file=file_personal).count(),
                'rejab': Rejab.objects.filter(file=file_personal).count(),
                'certificado_externo': CertificadoExterno.objects.filter(file=file_personal).count(),
                'certificado_empresa':  CertificadoAprobados.objects.filter(file=file_personal).count(),
                'certificado_academico': CertificadoAcademico.objects.filter(file=file_personal).count(),
                'convenios_contratos': ConveniosContratos.objects.filter(file=file_personal).count(),
                'pautas': PautasActuacion.objects.filter(file=file_personal).count(),
                'varios': Varios.objects.filter(file=file_personal).count(),
            }

            files.append({'persona': persona, 'documentos': documentos})

    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'files/documentos.html', {'files': files,'grupo':grupo})

def documento_empleados(request):
    personas = DatosPersonal.objects.filter(empleado_id=request.user)
    files = []
    for persona in personas:
        file_personal = FilePersonal.objects.filter(empleado_id=persona).first()
        if file_personal:
            documentos = {
                'id': file_personal.id_file,
                'hoja_vida': HojaVida.objects.filter(file=file_personal).count(),
                'foto': Foto.objects.filter(file=file_personal).count(),
                'croquis': Croquis.objects.filter(file=file_personal).count(),
                'memorandum': Memorandum.objects.filter(file=file_personal).count(),
                'carta_presentacion': CartaPresentacion.objects.filter(file=file_personal).count(),
                'varios': Varios.objects.filter(file=file_personal).count(),
                'carnet': Carnet.objects.filter(file=file_personal).count(),
                'luz_agua': LuzAgua.objects.filter(file=file_personal).count(),
                'induccion': Induccion.objects.filter(file=file_personal).count(),
                'curriculum': Curriculum.objects.filter(file=file_personal).count(),
                'felcc': Felcc.objects.filter(file=file_personal).count(),
                'felcn': Felcn.objects.filter(file=file_personal).count(),
                'rejab': Rejab.objects.filter(file=file_personal).count(),
                'certificado_externo': CertificadoExterno.objects.filter(file=file_personal).count(),
                'certificado_empresa':  CertificadoAprobados.objects.filter(file=file_personal).count(),
                'certificado_academico': CertificadoAcademico.objects.filter(file=file_personal).count(),
                'convenios_contratos': ConveniosContratos.objects.filter(file=file_personal).count(),
                'pautas': PautasActuacion.objects.filter(file=file_personal).count(),
                'varios': Varios.objects.filter(file=file_personal).count(),
            }
            files.append({'persona': persona, 'documentos': documentos})
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file=usuario.id_datos
    empleado_file = FilePersonal.objects.get(empleado_id=usuario_file)  
    foto = Foto.objects.filter(file=empleado_file.id_file).last()
    return render(request, 'files/documentos.html', {'files': files, 'grupo': grupo, 'foto':foto})






def get_documentos(request):
    documento_id = request.GET.get('documento_id')
    documento_type = request.GET.get('documento_type')
    if not documento_id or not documento_type:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    if documento_type == 'hoja_vida':
        documentos = HojaVida.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'croquis':
        documentos = Croquis.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'carnet':
        documentos = Carnet.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'felcc':
        documentos = Felcc.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'felcn':
        documentos = Felcn.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'rejap':
        documentos = Rejab.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'certificado_trabajo':
        documentos = CertificadoExterno.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'certificado_trabajo_empresa':
        documentos = CertificadoAprobados.objects.filter(file=documento_id)
    elif documento_type == 'certificado_academico':
        documentos = CertificadoAcademico.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'induccion':
        documentos = Induccion.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'carta':
        documentos = CartaPresentacion.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'convenios':
        documentos = ConveniosContratos.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'pautas':
        documentos = PautasActuacion.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'memorandum':
        documentos = Memorandum.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'varios':
        documentos = Varios.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'luz_agua':
        documentos = LuzAgua.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'curriculum':
        documentos = Curriculum.objects.filter(file=documento_id).select_related('clasificacion')
    elif documento_type == 'foto':
        documentos = Foto.objects.filter(file=documento_id).select_related('clasificacion')
    else:
        return JsonResponse({'error': 'Tipo de documento no válido'}, status=400)
    documentos_data = []
    for doc in documentos:
        if documento_type == 'hoja_vida':
            documento_info = {
                'id': doc.id_hoja,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas 
            }
        elif documento_type == 'foto':
            documento_info = {
                'id': doc.id_foto,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'carnet':
            documento_info = {
                'id': doc.id_carnet,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'luz_agua':
            documento_info = {
                'id': doc.id_factura_luz, 
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'curriculum':
            documento_info = {
                'id': doc.id_curriculum, 
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'croquis':
            documento_info = {
                'id': doc.id_croquis,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'felcc':
            documento_info = {
                'id': doc.id_felcc,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'felcn':
            documento_info = {
                'id': doc.id_felcn,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'rejap':
            documento_info = {
                'id': doc.id_rejab,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }
        elif documento_type == 'certificado_trabajo':
            documento_info = {
                'id': doc.id_certificado_externo,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            } 
        elif documento_type == 'certificado_trabajo_empresa':
            documento_info = {
                'id': doc.id_certificado_a,  
                'ruta': doc.drive if doc.drive else 'No disponible aun no Cargado en espera...',
                'fecha_registro': doc.fecha_emision.strftime('%d/%m/%Y'),
                'siglas': 'CT'
            } 
        elif documento_type == 'certificado_academico':
            documento_info = {
                'id': doc.id_certificado_academico,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'induccion':
            documento_info = {
                'id': doc.id_induccion,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'carta':
            documento_info = {
                'id': doc.id_carta_presentacion,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'convenios':
            documento_info = {
                'id': doc.id_convenios_contratos,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'pautas':
            documento_info = {
                'id': doc.id_pautas,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'memorandum':
            documento_info = {
                'id': doc.id_memorandum,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }  
        elif documento_type == 'varios':
            documento_info = {
                'id': doc.id_varios,  
                'ruta': doc.drive if doc.drive else 'No disponible',
                'fecha_registro': doc.fecha_registro.strftime('%d/%m/%Y'),
                'siglas': doc.clasificacion.siglas
            }   
        else:
            documento_info = {
                'error': 'Tipo de documento no encontrado'
            }

        documentos_data.append(documento_info)

    return JsonResponse({'documentos': documentos_data})

def perfil(request):
    grupos  = request.user.groups.first()
    grupo = grupos.name
    usuario = DatosPersonal.objects.get(empleado_id=request.user.id)
    usuario_file = usuario.id_datos
    files = FilePersonal.objects.get(empleado_id=usuario_file)
    foto = Foto.objects.filter(file=files.id_file).last()
    foto_persona = '/media/usuario.png'
    if foto:
        drive_url = foto.drive
        if '/view' in drive_url:
            file_id = drive_url.split('/d/')[1].split('/')[0]
            foto_persona = f"https://drive.google.com/thumbnail?id={file_id}"



    datos = usuario
    contacto = ContactosPersonal.objects.get(empleado_id=request.user.id)
    campos_llenos = 0
    campos_vacios = 0
    for field, value in usuario.__dict__.items():
        if not field.startswith('_'):
            if value:  
                campos_llenos += 1
            else:
                campos_vacios += 1
    campos_llenos_contacto = 0
    campos_vacios_contacto = 0
    for field, value in contacto.__dict__.items():
        if not field.startswith('_'):
            if value: 
                campos_llenos_contacto += 1
            else:
                campos_vacios_contacto += 1
    
    campos_vacios_contacto= campos_vacios_contacto-1
    datos_personales_completos = campos_llenos + campos_vacios
    datos_personales_porcentaje =  (campos_llenos / datos_personales_completos) * 100 
    contacto_completos = campos_llenos_contacto+campos_vacios_contacto
    contacto_porcentaje = (campos_llenos_contacto / contacto_completos) * 100  
    file_completos = 0
    file_incompletos = 0
    personas = DatosPersonal.objects.filter(empleado_id=request.user)
    files = []
    for persona in personas:
        file_personal = FilePersonal.objects.filter(empleado_id=persona).first()
        if HojaVida.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Foto.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Croquis.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Memorandum.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if CartaPresentacion.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Varios.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1  
        
        if Carnet.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1
        
        if LuzAgua.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Induccion.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Curriculum.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1
        
        if Felcc.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Felcn.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1
        
        if Rejab.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if CertificadoAprobados.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if CertificadoAcademico.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if ConveniosContratos.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if PautasActuacion.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1

        if Varios.objects.filter(file=file_personal).count()>0:
            file_completos+=1
        else:
            file_incompletos += 1
    total_files = file_completos + file_incompletos
    
    file_porcentaje = (file_completos / total_files) * 100 if total_files > 0 else 0
    request.session['datos_personales_porcentaje'] = datos_personales_porcentaje
    request.session['contacto_porcentaje'] = contacto_porcentaje
    request.session['file_porcentaje'] = file_porcentaje
    porcentaje_registro = (datos_personales_porcentaje + contacto_porcentaje + file_porcentaje)/3
    request.session['porcentaje_registro'] = porcentaje_registro
    context = {
        'grupo': grupo,
        'foto': foto_persona,
        
        'datos': datos,
        'contacto': contacto,
        'datos_personales_completos': datos_personales_completos,
        'datos_personales_incompletos': campos_vacios,
        'datos_personales_porcentaje': datos_personales_porcentaje,
        'contacto_completos': contacto_completos,
        'contacto_incompletos': campos_vacios_contacto,
        'contacto_porcentaje': contacto_porcentaje,
        'file_completos': file_completos,
        'file_incompletos': file_incompletos,
        'file_porcentaje': file_porcentaje,
    }
    return render(request, 'empleados/perfil.html', context)

def editar_datos_personal(request):
    return redirect( 'lista_empleados')

def nuevo_permiso(request):
    if request.method == 'POST':
        ver_dato = request.POST.get('ver')
        crear_dato = request.POST.get('crear')
        editar_dato = request.POST.get('editar')
        eliminar_dato = request.POST.get('eliminar')
        modulo_dato = request.POST.get('modulo')
        mod = Modulo.objects.get(id=modulo_dato)
        empleado_dato = request.POST.get('empleado')
        empl = User.objects.get(id=empleado_dato)
        if crear_dato == 'on':
            crear_dato = True
        else:
            crear_dato = False
   
        if editar_dato == 'on':
            editar_dato = True
        else:
            editar_dato = False

        if eliminar_dato == 'on':
            eliminar_dato = True
        else:
            eliminar_dato = False

        if ver_dato == 'on':
            ver_dato = True
        else:
            ver_dato = False
        permiso_registro = Permiso(
             
            empleado = empl,
            modulo = mod,
            ver = ver_dato,
            agregar = crear_dato,
            editar = editar_dato,
            eliminar = eliminar_dato
        )
        permiso_registro.save()
    return redirect('permisos')

def editar_empleado(request, id=None):
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        codigo_trabajador = request.POST.get('codigo_trabajador')
        nombre_trab = request.POST.get('nombre_trab')
        fecha_registro = request.POST.get('fecha_registro')
        empleado = get_object_or_404(Empleo, id=empleado_id)
        empleado.codigo_trabajador = codigo_trabajador
        empleado.nombre_trab = nombre_trab
        empleado.fecha_registro = fecha_registro
        empleado.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def obtener_empleo(request, id_empleo):
    empleo = get_object_or_404(Empleo, id_empleo=id_empleo)
    fecha_inicio = empleo.inicio_contrato
    fecha_actual = datetime.now().date() 
    antiguedad_anios = (fecha_actual - fecha_inicio).days // 365 
    clasificacion = ClasificacionAnti.objects.filter(
        rango_inicio__lte=antiguedad_anios, 
        rango_fin__gte=antiguedad_anios,
        activo=True
    ).first()  
    clasificacion_desc = clasificacion.descripcion if clasificacion else 'Sin clasificación'
    ultima_recontratacion = Empleo.objects.filter(
        codigo_trabajador=empleo.codigo_trabajador, 
        id_empleo__lt=id_empleo  
    ).order_by('-fecha_registro').first()
    ultima_recontratacion_fecha = ultima_recontratacion.inicio_contrato.strftime('%Y-%m-%d') if ultima_recontratacion else 'Sin recontratacion'
    nombre = empleo.empleado_id.empleado_id.first_name+' '+empleo.empleado_id.empleado_id.last_name
    code =  f"{empleo.empleado_id.ci}{empleo.empleado_id.expedido}"
    c_id = empleo.empleado_id.empleado_id.id
    c_asignado = AsignacionCorreosUsuarios.objects.filter(empleado = c_id).last()

    if c_asignado:
        c_dato = c_asignado.correo
        correos = c_dato
    else:
        correos = 'Sin Asignar'

    data = {
        'id': empleo.id_empleo,
        'codigo_trabajador': code,
        'nombre_trab': nombre,
        'fecha_registro': empleo.fecha_registro.strftime('%Y-%m-%d'),
        'inicio_contrato': empleo.inicio_contrato.strftime('%Y-%m-%d'),
        'modalidad': empleo.modalidad,
        'cargo': empleo.clasificacion.id_area,
        'correo_corp': correos,
        'numero_trabajo': empleo.numero_trabajo,
        'whatsapp': empleo.whatsapp,
        'interno': empleo.nro_interno,
        'clasificacion': clasificacion_desc, 
        'tipo_contrato': empleo.tipo_contrato.id_contrato if empleo.tipo_contrato.id_contrato else '',
        'tipo_registro': empleo.tipo_registro.id_registro if empleo.tipo_registro.id_registro else '',
        'activo': empleo.activo,
        'antiguedad_anios': antiguedad_anios, 
        'ultima_recontratacion': ultima_recontratacion_fecha, 
        'centro_trabajo': empleo.centro_trabajo.id_oficina
    }
    return JsonResponse(data)
 

def actualizar_empleo(request):
    if request.method == 'POST':
        try:
            id_empleo = request.POST.get('empleado_id')
            empleo = get_object_or_404(Empleo, id_empleo=id_empleo)
            codigo_trabajador = request.POST.get('codigo_trabajador')
            nombre_trab = request.POST.get('nombre_trab')
            fecha_registro = request.POST.get('fecha_registro')
            inicio_contrato = request.POST.get('inicio_contrato')
            celular = request.POST.get('celular')
            whatsapp = request.POST.get('whatsapp')
            trabajo = request.POST.get('trabajo')
            modalidad = request.POST.get('modalidad')
            cargo = request.POST.get('cargo_editar')
            interno = request.POST.get('interno')
            tipo_contrato = request.POST.get('tipo_contrato')
            contrato = TipoContrato.objects.get(id_contrato=tipo_contrato)    
            tipo_registro = request.POST.get('tipo_registro')
            registro = TipoRegistro.objects.get(id_registro=tipo_registro)
            fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date() if fecha_registro else None
            inicio_contrato = datetime.strptime(inicio_contrato, '%Y-%m-%d').date() if inicio_contrato else None
            empleo.codigo_trabajador = codigo_trabajador
            empleo.nombre_trab = nombre_trab
            empleo.fecha_registro = fecha_registro
            empleo.inicio_contrato = inicio_contrato
            empleo.modalidad = modalidad
            data = AreasCargos.objects.get(id_area = cargo)
            empleo.clasificacion = data
            empleo.tipo_contrato =  contrato
            empleo.numero_trabajo =  celular
            empleo.whatsapp =  whatsapp
            empleo.nro_interno =  interno
            empleo.tipo_registro =  registro
            marca = Oficina.objects.get(id_oficina = trabajo)
            empleo.centro_trabajo = marca
            empleo.save()
            return redirect(f"{reverse(datos_contratos)}?editar=true")

        except Exception as e:
            return redirect(f"{reverse(datos_contratos)}?error=true")
    
    return redirect(datos_contratos)   

def actualizar_empleado_empleado(request):
    if request.method == 'POST':
        id_empleo = request.POST.get('empleado_id')
        empleo = get_object_or_404(Empleo, id_empleo=id_empleo)
        codigo_trabajador = request.POST.get('codigo_trabajador')
        nombre_trab = request.POST.get('nombre_trab')
        fecha_registro = request.POST.get('fecha_registro')
        inicio_contrato = request.POST.get('inicio_contrato')
        celular = request.POST.get('celular')
        whatsapp = request.POST.get('whatsapp')
        modalidad = request.POST.get('modalidad')
        correo_corp = request.POST.get('correo_corp')
        interno = request.POST.get('interno')
        tipo_contrato = request.POST.get('tipo_contrato')
        contrato = TipoContrato.objects.get(id_contrato=tipo_contrato)    
        tipo_registro = request.POST.get('tipo_registro')
        registro = TipoRegistro.objects.get(id_registro=tipo_registro)
        fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date() if fecha_registro else None
        inicio_contrato = datetime.strptime(inicio_contrato, '%Y-%m-%d').date() if inicio_contrato else None
        empleo.codigo_trabajador = codigo_trabajador
        empleo.nombre_trab = nombre_trab
        empleo.fecha_registro = fecha_registro
        empleo.inicio_contrato = inicio_contrato
        empleo.modalidad = modalidad
        empleo.correo_corp = correo_corp
        empleo.tipo_contrato =  contrato
        empleo.numero_trabajo =  celular
        empleo.whatsapp =  whatsapp
        empleo.nro_interno =  interno
        empleo.tipo_registro =  registro
        empleo.save()
        return redirect('lista_empleados_empleados')  
    return redirect('lista_empleados_empleados')  


def actualizar_datos_contactos_empleado(request):
    if request.method == 'POST':
        id_contacto = request.POST.get('id_contacto')
        contactos = get_object_or_404(ContactosPersonal, id_contacto=id_contacto)
        telefono_2 = request.POST.get('telefono_2')
        telefono_1 = request.POST.get('telefono_1')
        grado_parentesco_2 = request.POST.get('grado_parentesco_2')
        grado_parentesco_1 = request.POST.get('grado_parentesco_1')
        contacto_2 = request.POST.get('contacto_2')
        contacto_1 = request.POST.get('contacto_1')
        Hijo1 = request.POST.get('Hijo1')
        ciudad_id = request.POST.get('ciudad')
        departamento_id = request.POST.get('departamento')
        departamento = Departamento.objects.get(id_depa = departamento_id)
        ciudad = Ciudad.objects.get(id_ciudad = ciudad_id)
        longitud = request.POST.get('longitud')
        latitud = request.POST.get('latitud')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        
        if 'foto_puerta' in request.FILES:
            foto_puerta = request.FILES['foto_puerta']
            nombre_archivo = f"foto_puertas/editados_{foto_puerta.name}"
            file_path = default_storage.save(nombre_archivo, foto_puerta)
            contactos.foto_puerta = file_path
        else:
            pass
        contactos.celular = telefono
        contactos.direccion = direccion
        contactos.latitud = latitud
        contactos.longitud = longitud
        contactos.contacto1_nombre = contacto_1
        contactos.contacto2_nombre = contacto_2
        contactos.contacto1_numero =  telefono_1
        contactos.contacto2_numero =  telefono_2
        contactos.contacto1_parentesco =  grado_parentesco_1
        contactos.contacto2_parentesco =  grado_parentesco_2
        contactos.ciudad =  ciudad
        contactos.departamento =  departamento
        contactos.hijos =  Hijo1
        contactos.mapa = True
        contactos.save()
        grupos_usuario = request.user.groups.first()
        grupo = grupos_usuario.name
        if grupo == 'Administradores':
            return redirect('personal_actual')  
        else:
            return redirect('personal_actual_empleado')  
    return redirect('personal_actual_empleado')   



def actualizar_datos_contactos(request):
    if request.method == 'POST':
        id_contacto = request.POST.get('id_contacto')
        contactos = get_object_or_404(ContactosPersonal, id_contacto=id_contacto)
        telefono_2 = request.POST.get('telefono_2')
        telefono_1 = request.POST.get('telefono_1')
        grado_parentesco_2 = request.POST.get('grado_parentesco_2')
        grado_parentesco_1 = request.POST.get('grado_parentesco_1')
        contacto_2 = request.POST.get('contacto_2')
        contacto_1 = request.POST.get('contacto_1')
        Hijo1 = request.POST.get('Hijo1')
        ciudad_id = request.POST.get('ciudad')
        departamento_id = request.POST.get('departamento')
        departamento = Departamento.objects.get(id_depa = departamento_id)
        ciudad = Ciudad.objects.get(id_ciudad = ciudad_id)
        longitud = request.POST.get('longitud')
        latitud = request.POST.get('latitud')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        foto_puerta = request.FILES.get('foto_puerta')
        if foto_puerta:
            nombre_archivo = f"foto_puertas/editados_{foto_puerta.name}"
            file_path = default_storage.save(nombre_archivo, foto_puerta)
            contactos.foto_puerta = file_path
        else:
            pass
        contactos.celular = telefono
        contactos.direccion = direccion
        contactos.latitud = latitud
        contactos.longitud = longitud
        contactos.contacto1_nombre = contacto_1
        contactos.contacto2_nombre = contacto_2
        contactos.contacto1_numero =  telefono_1
        contactos.contacto2_numero =  telefono_2
        contactos.contacto1_parentesco =  grado_parentesco_1
        contactos.contacto2_parentesco =  grado_parentesco_2
        contactos.ciudad =  ciudad
        contactos.departamento =  departamento
        contactos.hijos =  Hijo1
        contactos.save()
        grupos_usuario = request.user.groups.first()
        grupo = grupos_usuario.name
        return redirect('personal_actual')  
    
    return redirect('personal_actual')   


def listar_tipo_contrato(request):
    datos = TipoContrato.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/tipo_contrato.html', {'datos':datos,'grupo':grupo})

def listar_tipo_registro(request):
    datos = TipoRegistro.objects.all()
    grupos_usuario = request.user.groups.first()
    grupo = grupos_usuario.name
    return render(request, 'administracion/tipo_registro.html', {'datos':datos,'grupo':grupo})

def obtener_contactos(request, id_empleo):
    empleo = get_object_or_404(ContactosPersonal, id_contacto=id_empleo)
    ciudad_id = empleo.ciudad.id_ciudad if empleo.ciudad else None
    departamento_id = empleo.departamento.id_depa if empleo.departamento else None
    foto_puerta_url = empleo.foto_puerta.url if empleo.foto_puerta else None
    data = {
        'id_contacto': empleo.id_contacto,
        'celular': empleo.celular,
        'direccion': empleo.direccion,
        'latitud': empleo.latitud,
        'longitud': empleo.longitud,
        'contacto1_nombre': empleo.contacto1_nombre,
        'contacto1_numero': empleo.contacto1_numero,
        'contacto1_parentesco': empleo.contacto1_parentesco,
        'contacto2_nombre': empleo.contacto2_nombre,
        'contacto2_numero': empleo.contacto2_numero,
        'contacto2_parentesco': empleo.contacto2_parentesco,
        'ciudad': ciudad_id,
        'departamento': departamento_id,
        'hijos': empleo.hijos,
        'foto_puerta': foto_puerta_url,
        'activo': empleo.activo,
    }
    return JsonResponse(data)

def dato_empleados(request, id_empleo):
    empleo = get_object_or_404(DatosPersonal, id_datos=id_empleo)
 
    correo = User.objects.get(username=empleo.empleado_id)
    data = {
        'id_datos': empleo.id_datos,
        'ci': empleo.ci,
        'expedido': empleo.expedido,
        'nombre': empleo.nombre,
        'ap_paterno': empleo.ap_paterno,
        'ap_materno': empleo.ap_materno,
        'fecha_nacimiento': empleo.fecha_nacimiento.strftime('%Y-%m-%d'),
        'id_usuario': correo.id,
        'alergias': empleo.alergias,
        'correo': correo.email,
        'estado_civil': empleo.estado_civil.id_estado,
        'genero': empleo.genero.id_genero,
        'tipo_sangre': empleo.tipo_sangre,
        'activo': empleo.activo,
    }
    return JsonResponse(data)



def actualizar_datos_contactos(request):
    if request.method == 'POST':
        id_datos = request.POST.get('id_datos')
        datos = get_object_or_404(DatosPersonal, id_datos=id_datos)
          
        carnet_editar = request.POST.get('carnet_editar')
        expedido_editar = request.POST.get('expedido_editar')
        nombres = request.POST.get('nombres')
        ap_paterno_editar = request.POST.get('ap_paterno_editar')
        ap_materno_editar = request.POST.get('ap_materno_editar')
        fecha_registro_editar = request.POST.get('fecha_registro_editar')
        correo = request.POST.get('correo')
        alergias = request.POST.get('alergias')
        id_usuario = request.POST.get('id_usuario')
        user = get_object_or_404(User, id=id_usuario)
        civil_id = request.POST.get('civil')
        civil = EstadoCivil.objects.get(id_estado=civil_id)
        genero_id = request.POST.get('genero_editar')
        genero = Genero.objects.get(id_genero=genero_id)
        sangre_editar = request.POST.get('sangre_editar')
         

        user.email = correo 
        datos.ci = carnet_editar
        datos.expedido = expedido_editar
        datos.nombre = nombres
        datos.ap_paterno = ap_paterno_editar
        datos.ap_materno = ap_materno_editar
        datos.fecha_nacimiento = fecha_registro_editar
        datos.alergias =  alergias
        datos.estado_civil =  civil
        datos.genero =  genero
        datos.tipo_sangre =  sangre_editar
        user.save()
        datos.save()
        grupos_usuario = request.user.groups.first()
        grupo = grupos_usuario.name
        return redirect('lista_maestra')  
    
    return redirect('lista_maestra')   


def actualizar_datos_admin(request):
    if request.method == 'POST':
        try:
            id_datos = request.POST.get('id_datos')
            datos = get_object_or_404(DatosPersonal, id_datos=id_datos)
            
            carnet_editar = request.POST.get('carnet_editar')
            expedido_editar = request.POST.get('expedido_editar')
            nombres = request.POST.get('nombres')
            ap_paterno_editar = request.POST.get('ap_paterno_editar')
            ap_materno_editar = request.POST.get('ap_materno_editar')
            fecha_registro_editar = request.POST.get('fecha_registro_editar')
            correo = request.POST.get('correo')
            alergias = request.POST.get('alergias')
            id_usuario = request.POST.get('id_usuario')
            user = get_object_or_404(User, id=id_usuario)
            civil_id = request.POST.get('civil')
            civil = EstadoCivil.objects.get(id_estado=civil_id)
            genero_id = request.POST.get('genero_editar')
            genero = Genero.objects.get(id_genero=genero_id)
            sangre_editar = request.POST.get('sangre_editar')
            

            user.email = correo 
            datos.ci = carnet_editar
            datos.expedido = expedido_editar
            datos.nombre = nombres
            datos.ap_paterno = ap_paterno_editar
            datos.ap_materno = ap_materno_editar
            datos.fecha_nacimiento = fecha_registro_editar
            datos.alergias =  alergias
            datos.estado_civil =  civil
            datos.genero =  genero
            datos.tipo_sangre =  sangre_editar
            datos.completo = True
            user.save()
            datos.save()
            grupos_usuario = request.user.groups.first()
            grupo = grupos_usuario.name
            
            return redirect(f"{reverse('lista_empleados')}?editar=true")

        except Exception as e:
            return redirect(f"{reverse('lista_empleados')}?error=true")
        
    return redirect('lista_empleados')   



def obtener_usuario(request, id_empleo):
    try:
        usuario = User.objects.get(id=id_empleo)
        grupos_usuario = usuario.groups.first()
 

        data = {
            'id': usuario.id,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'email': usuario.email,
            'username': usuario.username,
            'password': usuario.password, 
            'rol': grupos_usuario.id,
        }
    
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    


def actualizar_datos_usuario(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_user_edit')
            usuario = get_object_or_404(User, id=id)
            first_name = request.POST.get('nombre_editar')
            email = request.POST.get('email_editar')
            last_name = request.POST.get('apellido_editar')
            username = request.POST.get('usuario_editar')
            password = request.POST.get('password_editar')
            password_confirm = request.POST.get('password_editar_confirmar')
            rol = request.POST.get('rol_editar')
            usuario.first_name = first_name
            usuario.email = email
            usuario.last_name = last_name
            usuario.username = username
            if password:
                if password != password_confirm:
                    messages.error(request, "Las contraseñas no coinciden.")
                    return redirect('empleados') 
                usuario.set_password(password)  

            if rol:
                usuario.groups.clear()
                try:
                    grupo = Group.objects.get(id=rol)
                    usuario.groups.add(grupo)  
                except Group.DoesNotExist:
                    messages.error(request, "El rol seleccionado no existe.")
                    return redirect('empleados')   
            usuario.save()
            return redirect(f"{reverse('empleados')}?editar=true")

        except Exception as e:
            return redirect(f"{reverse('empleados')}?error=true")
  
    return redirect("empleados")

def detalle_equipo(request):
    return render(request, 'equipos/detalle.html')


def listar_equipos(request):
    datos = Equipos.objects.all()
    asignados = Asignacion.objects.all()
    usuarios = User.objects.all().order_by('first_name')
    return render(request, 'equipos/listar_equipos.html', {'datos':datos, 'usuarios':usuarios})

def buscar_equipo(request):
    equipos = Equipos.objects.all()
    
    return render(request, 'equipos/buscar.html', {'datos':equipos})



def detalle_2(request):

    return render(request, 'equipos/detalle_2.html' )

def detalle_equipo_2(request):
    qr_code_url = None
    if request.method == "POST":
        data = request.POST.get("qr_data", "")
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            file_path = os.path.join(settings.MEDIA_ROOT, "qr.png")
            img.save(file_path)
            qr_code_url = f"{settings.MEDIA_URL}qr.png"

 
    return render(request, 'equipos/detalle_2.html', {'qr_code_url': qr_code_url})

def registrar_equipo(request):
    qr_code_url = None
    if request.method == "POST":
        data = request.POST.get("qr_data", "")
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            file_path = os.path.join(settings.MEDIA_ROOT, "qr/qr.png")
            img.save(file_path)
            qr_code_url = f"{settings.MEDIA_URL}qr.png"

    
    return render(request, 'equipos/registrar_equipo.html', {'qr_code_url': qr_code_url})

def generar_contrasena(longitud=13, palabra_clave=""):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud - len(palabra_clave)))
    contrasena += palabra_clave 
    return contrasena


def generar_contrasenas(request):
    cuentas = usuarioCorreos.objects.all()
    usuarios = User.objects.filter(is_active = True)   
    return render(request, 'cuentas/generar_contrasenas.html', {
         
        'usuarios': usuarios,
        'datos':cuentas,
    })


def agregar_equipo(request):
    if request.method == 'POST':
        nombre_equipo = request.POST.get('nombre_equipo')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        tipo = request.POST.get('tipo')
        tamano = request.POST.get('tamano')
        fecha_compra = request.POST.get('fecha_registro')
        if isinstance(fecha_compra, str):
            fecha_compra = datetime.strptime(fecha_compra, '%Y-%m-%d').date()
        fecha_registro = timezone.now()
        descripcion = request.POST.get('descripcion')
        componentes = request.POST.get('componentes')
        equipo = Equipos()
        equipo.nombre = nombre_equipo
        equipo.marca = marca
        equipo.descripcion = descripcion
        equipo.modelo = modelo
        equipo.tipo = tipo
        equipo.tamano = tamano
        equipo.fecha_compra = fecha_compra
        fecha_registro=fecha_registro.date()
        anti =  fecha_registro -fecha_compra
        equipo.fecha_registro = fecha_registro
        equipo.auxiliares = componentes
        if anti.days >= 60:
            equipo.antiguo = True
        else:
            equipo.antiguo = False
        equipo.save()
        imagenes = request.FILES.getlist('fotos')
        if imagenes:
            for idx, imagen in enumerate(imagenes[:5]): 
                campo_imagen = f"imagen_{idx}"  
                print(f'[DEBUG] Procesando imagen {idx}')
                directorio = os.path.join(settings.MEDIA_ROOT, 'equipos', str(equipo.id_equipo))
                if not os.path.exists(directorio):
                    os.makedirs(directorio)  
                nombre_archivo = f"{equipo.id_equipo}_{imagen.name}"
                file_path = os.path.join('equipos', str(equipo.id_equipo), nombre_archivo)
                file_path = default_storage.save(file_path, imagen)
                print(f'[DEBUG] Imagen guardada en: {file_path}')
                setattr(equipo, campo_imagen, file_path)
                
            equipo.save()  

        id_equipo = equipo.id_equipo
        datos = Equipos.objects.get(id_equipo=id_equipo)
        qr_code_url = None
        data = f"media/qr/{datos.id_equipo}.png"
        info = f"{settings.BASE_URL_QR}/ver_equipo/{datos.id_equipo}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(info)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        text = f"VLSC-SIS-{datos.id_equipo}"
        datos.codigo_equipo = text
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 30)   
        except IOError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0] 
        text_height = bbox[3] - bbox[1]  
        qr_width, qr_height = img.size
        text_x = (qr_width - text_width) // 2
        text_y = qr_height - text_height - 10  
        draw.text((text_x, text_y), text, font=font, fill="black")
        img.save(os.path.join(settings.MEDIA_ROOT, 'qr', f"{datos.id_equipo}.png"))
        datos.qr = data
        datos.save()

        clave = Fernet.generate_key()
        aux =  datos.codigo_equipo
        mensaje = aux.encode()
        f = Fernet(clave)
        encriptado = f.encrypt(mensaje)
        asunto = base64.urlsafe_b64encode(encriptado).decode('utf-8')
        marca = base64.urlsafe_b64encode(clave).decode('utf-8')

        empl = AsignadoEquipoCuenta()
        empl.codigo_equipo =  aux
       
        empl.fecha_cambio  = timezone.now()
        empl.estado = 1
        empl.clave = marca
        empl.save()
        cuenta = EquiposCuentas()
        cuenta.equipo_id = equipo
        cuenta.fecha = timezone.now()
        tipo_cuenta = TipoContrasenaEquipos.objects.get(id_tipo=1)
        cuenta.tipo = tipo_cuenta
        cuenta.datos = asunto
        cuenta.usuario_cuenta = nombre_equipo
        cuenta.asignado_id = empl
        nombre_aux = request.user
        cuenta.encargado = nombre_aux
        cuenta.save()

        backup = EstadoBackups()
        backup.fecha = timezone.now()
        backup.equipo = equipo
        backup.estado = 1
        backup.usuario = request.user
        backup.save()


        return redirect('listar_equipos')

    return redirect('listar_equipos')

def ver_equipo(request, id_equipo):
    try:
        equipo = Equipos.objects.get(id_equipo=id_equipo)
        if equipo.asignacion:
            nombre = equipo.asignacion.empleado.first_name+' '+ equipo.asignacion.empleado.last_name
        else:
            nombre = 'Sin Asignar'

        equipos_auxiliares = equipo.auxiliares.split(',')
        data = {
            'id_equipo': equipo.id_equipo,
            'nombre': equipo.nombre,
            'marca': equipo.marca,
            'modelo': equipo.modelo,
            'descripcion': equipo.descripcion,
            'tipo': equipo.tipo,
            'fecha_nacimiento': equipo.fecha_registro.strftime('%Y-%m-%d'),
            'tamano': equipo.tamano,
            'qr': equipo.qr,
            'imagen_0' : equipo.imagen_0,
            'imagen_1' : equipo.imagen_1,
            'imagen_2' : equipo.imagen_2,
            'imagen_3' : equipo.imagen_3,
            'imagen_4' : equipo.imagen_4,
            'asignado': nombre,
            'codigo_equipo' : equipo.codigo_equipo
        }
        asignados = Asignacion.objects.filter(equipo = equipo.codigo_equipo)
        devueltos = DevolucionEquipo.objects.filter(equipo = equipo.codigo_equipo)
       
        return render(request, 'equipos/detalle.html', {'datos': data, 'equipos_auxiliares':equipos_auxiliares, 'asignados':asignados, 'devueltos': devueltos})
    
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
    
def ver_equipo_codigo(request, codigo):
    try:
        asignacion = Asignacion.objects.get(id_asignacion=codigo)
        marca = asignacion.equipo

        equipo = Equipos.objects.get(codigo_equipo=marca)
        if equipo.asignacion:
            nombre = equipo.asignacion.empleado.first_name+' '+ equipo.asignacion.empleado.last_name
        else:
            nombre = 'Sin Asignar'

        equipos_auxiliares = equipo.auxiliares.split(',')
        data = {
            'id_equipo': equipo.id_equipo,
            'nombre': equipo.nombre,
            'marca': equipo.marca,
            'modelo': equipo.modelo,
            'descripcion': equipo.descripcion,
            'tipo': equipo.tipo,
            'fecha_nacimiento': equipo.fecha_registro.strftime('%Y-%m-%d'),
            'tamano': equipo.tamano,
            'qr': equipo.qr,
            'imagen_0' : equipo.imagen_0,
            'imagen_1' : equipo.imagen_1,
            'imagen_2' : equipo.imagen_2,
            'imagen_3' : equipo.imagen_3,
            'imagen_4' : equipo.imagen_4,
            'asignado': nombre,
            'codigo_equipo' : equipo.codigo_equipo
        }
        asignados = Asignacion.objects.filter(equipo = equipo.codigo_equipo)
        devueltos = DevolucionEquipo.objects.filter(equipo = equipo.codigo_equipo)
       
        return render(request, 'equipos/detalle.html', {'datos': data, 'equipos_auxiliares':equipos_auxiliares, 'asignados':asignados, 'devueltos': devueltos})
    
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
    

def guardar(request):
    return render(request, 'equipos/guardar.html')


def mostrar_equipo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
  
        asignados = Asignacion.objects.filter(equipo = codigo)
        devueltos = DevolucionEquipo.objects.filter(equipo = codigo)
        imagen_qr = request.POST.get('imagen_qr')
        if codigo:
            datos = Equipos.objects.get(codigo_equipo=codigo)
            equipos_auxiliares = datos.auxiliares.split(',')
        else:
            datos = None

        return render(request, 'equipos/buscar.html', {'datos':datos, 'equipos_auxiliares': equipos_auxiliares, 'asignados':asignados, "devueltos":devueltos})
        
    else:
        return redirect('buscar_equipo')
 

def obtener_datos_equipo(request, datos_id):
    try:
        datos_obt = Equipos.objects.get(id_equipo=datos_id)
        data = {
            
          
            'codigo_equipo': datos_obt.codigo_equipo,
        
        }
 
        return JsonResponse(data)
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def obtener_datos_equipo2(request, datos_id):
    try:
        datos_obt = Equipos.objects.get(id_equipo=datos_id)
        data = {
            
            'empleado_id': datos_obt.asignacion.empleado.id,
            'empleado': datos_obt.asignacion.empleado.first_name+" "+datos_obt.asignacion.empleado.last_name,
   
            'codigo_equipo_devolver': datos_obt.codigo_equipo,
        }
 
        return JsonResponse(data)
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def obtener_datos_equipo3(request, datos_id):
    try:
        asignacion = Asignacion.objects.get(id_asignacion =datos_id)
        marca = asignacion.equipo
        datos_obt = Equipos.objects.get(codigo_equipo=marca)
        data = {
            
            'empleado_id': datos_obt.asignacion.empleado.id,
            'empleado': datos_obt.asignacion.empleado.first_name+" "+datos_obt.asignacion.empleado.last_name,
   
            'codigo_equipo_devolver': datos_obt.codigo_equipo,
        }
 
        return JsonResponse(data)
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)

def obtener_datos_correo_uni(request, id):
    try:
        datos = usuarioCorreos.objects.get(id_u_correo =id)
        data = {
            'correo_encontrado': datos.correo_usuario,
            'id_correo_uni' : datos.id_u_correo,
        }
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)

def obtener_datos_correo_multi(request, id):
    try:
        datos = usuarioCorreos.objects.get(id_u_correo =id)
        data = {
            'correo_encontrado_multi': datos.correo_usuario,
            'id_correo_multi' : datos.id_u_correo,
        }
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)

def obtener_datos_correo_multi2(request, id):
    try:
        datos = usuarioCorreos.objects.get(id_u_correo =id)
        data = {
            'correo_encontrado_multi2': datos.correo_usuario,
            'id_correo_multi2' : datos.id_u_correo,
        }
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)



def asignar_equipo(request):
    if request.method == 'POST':
        equipo = request.POST.get('codigo_equipo')
        empleado_asignado = request.POST.get('empleado_asignado')
        asignacion = request.POST.get('asignacion')
        
        detalle = request.POST.get('detalle')
        equipo_leido = Equipos.objects.get(codigo_equipo=equipo)
        if equipo_leido.estado == False :
            datos = Asignacion()
            datos.equipo = equipo
            datos_user = User.objects.get(id=empleado_asignado)
            datos.empleado = datos_user
            datos.fecha_asignado = asignacion
            if request.POST.get('devolucion'):
                devolucion = request.POST.get('devolucion')
                datos.fecha_devuelto = devolucion
            datos.estado = False
            datos.detalle = detalle
            datos.save()
            equipo_leido.estado = True
            equipo_leido.asignacion = datos
            equipo_leido.save()
    

    return redirect(listar_equipos)
    
def devolver_equipo(request):
    if request.method == 'POST':
        equipo = request.POST.get('codigo_equipo_devolver')
        empleados_usuario = request.POST.get('empleado_devolver')
        observacion_devolver = request.POST.get('observacion_devolver')
        
        datos_user = User.objects.get(id=empleados_usuario)
        asignado = Asignacion.objects.filter(equipo=equipo).last()
        fecha = timezone.now()
        fecha_calculo = fecha.date()
        fecha_inicial = asignado.fecha_asignado 
        lapso = fecha_calculo-fecha_inicial
        lapso_en_dias = lapso.days
        if lapso_en_dias < 1:
            lapso_en_dias = 1

        equipo_leido = Equipos.objects.get(codigo_equipo=equipo)
        if equipo_leido.estado == True:
            datos = DevolucionEquipo()
            datos.fecha = fecha
            datos.empleado = datos_user
            datos.lapzo = lapso_en_dias
            datos.equipo = equipo
            datos.observaciones = observacion_devolver
            
            datos.save()
            asignado.estado = True
            asignado.devolucion = datos
            asignado.save()
            equipo_leido.estado = False
            equipo_leido.asignacion = None
            equipo_leido.save()
    

    return redirect(listar_equipos)
    

def devolver_equipo_buscado(request):
    if request.method == 'POST':
        equipo = request.POST.get('codigo_equipo_devolver')
        empleados_usuario = request.POST.get('empleado_devolver')
        observacion_devolver = request.POST.get('observacion_devolver')
        
        datos_user = User.objects.get(id=empleados_usuario)
        asignado = Asignacion.objects.filter(equipo=equipo).last()
        fecha = timezone.now()
        fecha_calculo = fecha.date()
        fecha_inicial = asignado.fecha_asignado 
        lapso = fecha_calculo-fecha_inicial
        lapso_en_dias = lapso.days
        if lapso_en_dias < 1:
            lapso_en_dias = 1

        equipo_leido = Equipos.objects.get(codigo_equipo=equipo)
        if equipo_leido.estado == True:
            datos = DevolucionEquipo()
            datos.fecha = fecha
            datos.empleado = datos_user
            datos.lapzo = lapso_en_dias
            datos.equipo = equipo
            datos.observaciones = observacion_devolver
            
            datos.save()
            asignado.estado = True
            asignado.devolucion = datos
            asignado.save()
            equipo_leido.estado = False
            equipo_leido.asignacion = None
            equipo_leido.save()
    

    return redirect(buscar_empleado_equipo)
    

def info_equipos_editar(request, id_datos):
    try:
        datos_editar = Equipos.objects.get(id_equipo=id_datos)
        data = {
            'id_equipo': datos_editar.id_equipo,
            'marca': datos_editar.marca,
            'nombre': datos_editar.nombre,
            'descripcion': datos_editar.descripcion,
            'tipo': datos_editar.tipo,
            'tamano': datos_editar.tamano,
            'modelo': datos_editar.modelo,
            'fecha_compra': datos_editar.fecha_compra.strftime('%Y-%m-%d'),
            'auxiliares': datos_editar.auxiliares,
        }
 
        return JsonResponse(data)
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def mantenimiento(request):
    datos = Mantenimientos.objects.all()
    usuarios = User.objects.filter(is_active = True)
    equipos = Equipos.objects.filter(activo = True)
    return render(request,'equipos/mantenimiento.html', {'datos':datos, 'usuarios': usuarios, 'equipos':equipos})


def buscar_empleado_equipo(request):
    equipos = [] 
    empleados = User.objects.all()
    codigos = DatosPersonal.objects.exclude(ci=None)
    no_equipo_message = ''
    if request.method == 'POST':
        id_empleado = request.POST.get('empleado_nombre')
        codigo = request.POST.get('codigo_empleado_equipo')
      
        if id_empleado:
            equipos = Asignacion.objects.filter(empleado=id_empleado)
            nombre = User.objects.get(id=id_empleado)
            no_equipo_message = nombre.first_name +" "+ nombre.last_name
        
        elif codigo:
            equipos = Asignacion.objects.filter(empleado=codigo) 
            nombre = User.objects.get(id=codigo) 
            no_equipo_message = nombre.first_name +" "+ nombre.last_name
 

    return render(request, 'equipos/buscar_empleado_equipo.html', {
        'datos': equipos,
        'empleados': empleados,
        'codigos': codigos,
        'no_equipo_message': no_equipo_message  
    })


def editar_equipo(request):
    if request.method == 'POST':
        id_equipo = request.POST.get('id_equipo')
        nombre_equipo = request.POST.get('nombre_equipo_editar')
        marca = request.POST.get('marca_editar')
        modelo = request.POST.get('modelo_editar')
        tipo = request.POST.get('tipo_editar')
        tamano = request.POST.get('tamano_editar')
        fecha_compra = request.POST.get('fecha_registro_editar')
        if isinstance(fecha_compra, str):
            fecha_compra = datetime.strptime(fecha_compra, '%Y-%m-%d').date()
        fecha_registro = timezone.now()
        descripcion = request.POST.get('descripcion_editar')
        equipo = Equipos.objects.get(id_equipo=id_equipo)
        equipo.nombre = nombre_equipo
        equipo.marca = marca
        equipo.descripcion = descripcion
        equipo.modelo = modelo
        equipo.tipo = tipo
        equipo.tamano = tamano
        equipo.fecha_compra = fecha_compra
        fecha_registro=fecha_registro.date()
        anti =  fecha_registro -fecha_compra
        equipo.fecha_registro = fecha_registro
        if anti.days >= 60:
            equipo.antiguo = True
        else:
            equipo.antiguo = False
       
        imagenes = request.FILES.getlist('fotos_editar')
        if imagenes:
            for idx, imagen in enumerate(imagenes[:5]): 
                campo_imagen = f"imagen_{idx}"  
                directorio = os.path.join(settings.MEDIA_ROOT, 'equipos', str(equipo.id_equipo))
                if not os.path.exists(directorio):
                    os.makedirs(directorio)  
                nombre_archivo = f"{equipo.id_equipo}_{imagen.name}"
                file_path = os.path.join('equipos', str(equipo.id_equipo), nombre_archivo)
                file_path = default_storage.save(file_path, imagen)
                setattr(equipo, campo_imagen, file_path)   
        
        equipo.save()  

    return redirect('listar_equipos')


def agregar_usuario_correo(request):
    if request.method == 'POST':
        try:
            fecha_asignado = request.POST.get('fecha_asignado')
            tipo = request.POST.get('tipo')
            correo = request.POST.get('correo')
            alias_correo = request.POST.get('alias_correo')
            observaciones = request.POST.get('observaciones')
            password = request.POST.get('password')
            password_confirmar = request.POST.get('password_confirmar')  

            if password != password_confirmar:
                return render(request, 'cuentas/generar_contrasenas.html', {
                    'usuarios': usuarios,
                    'datos': cuentas,
                    'error': 'Las contraseñas no coinciden'})


            
            dato = usuarioCorreos()
        
            dato.fecha = fecha_asignado

            clave = Fernet.generate_key()

            mensaje = password.encode()

            f = Fernet(clave)
            encriptado = f.encrypt(mensaje)
            
            desen = f.decrypt(encriptado)
            
            dato.asunto = base64.urlsafe_b64encode(encriptado).decode('utf-8')
            dato.tipo = tipo
            dato.correo_usuario = correo
            dato.compartido = alias_correo
            dato.observacion = observaciones
            dato.estado = 0
            dato.save()
            control = controlUsuario()
            control.fecha = timezone.now()
            control.detalle = 'creacion de usuario a cuenta'
            control.registro = dato
            control.usuario = request.user
            control.marca = base64.urlsafe_b64encode(clave).decode('utf-8')
            control.tipo = 1
            control.save()
    
            estado = EstadoBackupsCorreos()
            estado.correo = dato
            estado.usuario = request.user
            estado.fecha = timezone.now()
            estado.save()

    
            return redirect(f"{reverse(generar_contrasenas)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(generar_contrasenas)}?error=true")
    


    cuentas = usuarioCorreos.objects.all()
    usuarios = User.objects.all()   
    return render(request, 'cuentas/generar_contrasenas.html', {
        'usuarios': usuarios,
        'datos': cuentas,
    })



def control_crud(request):
    
    usuarios = User.objects.all()
    return render(request, 'cuentas/control.html', {
        'usuarios': usuarios,
       
    })


def lista_control_crud(request):
    usuarios = User.objects.all()
    datos = controlUsuario.objects.all()
    return render(request, 'cuentas/control.html', {
        'usuarios': usuarios,
        'datos':datos,
    })




def generar_codigo():
    return ''.join(random.choices(string.digits, k=10))

def enviar_codigo(request):
    if request.method == "POST":
        correo_principal = settings.BASE_CORREO
        codigo = generar_codigo()
        send_mail(
            'Código de verificación',
            f'Tu código de verificación es: {codigo}',
            correo_principal,
            [correo_principal],
            fail_silently=False,
        )
        control = controlUsuario()
        control.fecha = timezone.now()
        control.detalle = 'Solicitud de codigo para ver contrasena'
        control.usuario = request.user
        control.tipo = 3
        control.save()
        verificacion = VerificacionCodigo(codigo=codigo, tiempo_expiracion=now())
        verificacion.save()
        return JsonResponse({"success": True, "message": "El Código fue enviado correctamente a tu cuenta gmail revisa tu bandeja de entrada", "codigo": codigo})

def verificar_codigo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get('codigo_ingresado')
        data_id = request.POST.get('data') 
        registro = controlUsuario.objects.filter(registro = data_id).last()
        registro2 = usuarioCorreos.objects.filter(id_u_correo = data_id).last()
        clave_guardada = base64.urlsafe_b64decode(registro.marca.encode('utf-8')) 
        f = Fernet(clave_guardada)
        asunto_cifrado = base64.urlsafe_b64decode(registro2.asunto.encode('utf-8'))
        mensaje_desencriptado = f.decrypt(asunto_cifrado).decode('utf-8')
        verificacion = VerificacionCodigo.objects.last()
        if verificacion and verificacion.codigo == codigo_ingresado:
            tiempo_restante = (now() - verificacion.tiempo_expiracion).seconds
            if tiempo_restante <= 180:  
                return JsonResponse({
                    'success': True,
                    'codigo': mensaje_desencriptado,
                    'message': 'Código verificado correctamente'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'El código ha expirado'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Código incorrecto'
            })

    return redirect('credencial')  




def check_marcados(request):
    if request.method == 'POST':
        ids_seleccionados = request.POST.get('ids_seleccionados', '').split(',')
        correos = usuarioCorreos.objects.filter(id_u_correo__in=ids_seleccionados)
        for correo in correos:
            clave = Fernet.generate_key()
            password = generar_contrasena()
            mensaje = password.encode()
            f = Fernet(clave)
            encriptado = f.encrypt(mensaje)
            datos_prev = correo.asunto
            correo.asunto = base64.urlsafe_b64encode(encriptado).decode('utf-8')
            correo.save()
            control = controlUsuario()
            control.fecha = timezone.now()
            control.detalle = 'cambio de contrasena en cuenta'
            control.registro = correo
            control.usuario = request.user
            control.marca = base64.urlsafe_b64encode(clave).decode('utf-8')
            control.tipo = 2
            control.anterior = datos_prev
            control.save()
    return redirect(generar_contrasenas)

from django.utils import timezone

def check_informe(request):
    if request.method == 'POST':
        ids_seleccionados = request.POST.get('ids_seleccionados_info', '').split(',')
        correos = usuarioCorreos.objects.filter(id_u_correo__in=ids_seleccionados)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        header_style = ParagraphStyle(
            'HeaderStyle',
            fontSize=10,   
            fontName='Helvetica-Bold',
            alignment=1,   
            spaceAfter=10,
        )
        current_time = timezone.now()  
        current_time_aware = timezone.make_aware(current_time, timezone.get_current_timezone())  # Aseguramos que sea "aware"
        elements.append(Table([['La Paz,', timezone.localtime(current_time_aware).strftime('%d/%m/%Y %H:%M:%S')]], colWidths=[500], rowHeights=[50]))
        elements.append(Table([['']]))
        data = [
            ['Fecha', 'Correo Asignado','Codigo cuenta']
        ]
        for correo in correos:
            control = controlUsuario.objects.filter(registro=correo.id_u_correo).last()
            clave_guardada = base64.urlsafe_b64decode(control.marca.encode('utf-8')) 
            f = Fernet(clave_guardada)
            asunto_cifrado = base64.urlsafe_b64decode(correo.asunto.encode('utf-8'))
            fecha_asignado = correo.fecha
            usuario_correo = correo.correo_usuario
            codigo = f.decrypt(asunto_cifrado).decode('utf-8')
            tipo = correo.tipo
            
            data.append([fecha_asignado, usuario_correo,codigo])

        control = controlUsuario()
        control.fecha = timezone.now()
        control.detalle = 'Solicitud de Informe de Usuarios'
        control.usuario = request.user
        control.tipo = 4
        control.save()
        
        table = Table(data, colWidths=[70, 130, 130, 100, 130])   
        table.setStyle(TableStyle([ 
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        for i in range(len(data[0])):
            table.setStyle(TableStyle([
                ('FONTNAME', (i, 0), (i, 0), 'Helvetica-Bold'),   
                ('FONTSIZE', (i, 1), (-1, -1), 6)   
            ]))

        elements.append(table)
        doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Enviar el correo con el archivo PDF adjunto
        email = EmailMessage(
            'Informe de Correos',
            'Adjunto se encuentra el informe solicitado.',
            settings.BASE_CORREO,  
            [settings.BASE_CORREO] 
        )
        email.attach('informe.pdf', pdf_content, 'application/pdf')
        email.send()

        # Redirigir después de enviar el informe
        return redirect('generar_contrasenas')




def asignar_correo_uni(request):
    if request.method == 'POST':
        select_empleado_1 = request.POST.get('select_empleado_1')
        asignacion_uni = request.POST.get('asignacion_uni')
    
        if request.POST.get('asignacion_alias_uni')== 'Sin alias':
            alias = 'Sin alias'
        else: 
            alias = request.POST.get('asignacion_alias_uni')

        detalle_uni = request.POST.get('detalle_uni')
        correo_id = request.POST.get('id_correo_uni')
        correo_nombre = request.POST.get('correo_uni')
        marca = usuarioCorreos.objects.get(id_u_correo=correo_id)
        marca.estado = 1
        

        empl = User.objects.get(id=select_empleado_1)
        datos = AsignacionCorreosUsuarios()
        datos.correo  = correo_nombre
        datos.fecha = asignacion_uni
        datos.empleado = empl
        datos.observacion = detalle_uni
        datos.estado = True
        datos.save()
        # obtener= DatosPersonal.objects.get(empleado_id=select_empleado_1)
        # print('DEBUG OBTENIDO')
        # print(obtener)
        # contrato = Empleo.objects.get(empleado_id = obtener.id_datos)
        # print('DEBUG OBTENIDO')
        # print(contrato)
        # contrato.correo_corp = datos
        # print('DEBUG OBTENIDO')
        # print(datos)
        # contrato.save()

        marca.asignado = datos
         
        marca.save()
        return redirect('generar_contrasenas')
            
    return redirect('generar_contrasenas')



def asignar_correo_multi(request):
    if request.method == 'POST':
        
        select_empleado_1 = request.POST.get('select_empleado_2')
        asignacion_uni = request.POST.get('asignacion_multi')
        alternativo = request.POST.get('correo-alias_multi')
      
        detalle_uni = request.POST.get('detalle_multi')
        correo_id = request.POST.get('id_correo_multi')
        marca = usuarioCorreos.objects.get(id_u_correo=correo_id)
        
        nuevo = usuarioCorreos()
        nuevo.correo_usuario = marca.correo_usuario
        nuevo.fecha = timezone.now()
        nuevo.observacion = 'Cuenta Alias de la cuenta :'+ marca.correo_usuario
        nuevo.correo_alt = alternativo
        nuevo.tipo = marca.tipo

        nuevo.estado = 1
        
        empl = User.objects.get(id=select_empleado_1)
        datos = AsignacionCorreosUsuarios()
        datos.correo = nuevo.correo_usuario
        datos.fecha = asignacion_uni
        datos.correo_alt = alternativo
        datos.empleado = empl
        datos.observacion = detalle_uni
        datos.save()
        nuevo.asignado = datos
        nuevo.save()
        
        marca.estado = 2
        marca.save()

        # obtener= DatosPersonal.objects.get(empleado_id=select_empleado_1)
        # print('DEBUG OBTENIDO')
        # print(obtener)
        # contrato = Empleo.objects.get(empleado_id = obtener.id_datos)
        # print('DEBUG OBTENIDO')
        # print(contrato)
        # contrato.correo_corp = datos
        # print('DEBUG OBTENIDO')
        # print(datos)
        # contrato.save()
        return redirect('generar_contrasenas')
            
    return redirect('generar_contrasenas')


def asignar_correo_multi2(request):
    if request.method == 'POST':
        select_empleado_1 = request.POST.get('select_empleado_3')
        asignacion_uni = request.POST.get('asignacion_multi2')
        
        alternativo = request.POST.get('correo-alias_multi2')
    
        detalle_uni = request.POST.get('detalle_multi2')
        correo_id = request.POST.get('id_correo_multi2')
        marca = usuarioCorreos.objects.get(id_u_correo=correo_id)
        marca.estado = 2
        marca.save()
        empl = User.objects.get(id=select_empleado_1)
        datos = AsignacionCorreosUsuarios()
        datos.correo = marca
        datos.fecha = asignacion_uni
        datos.correo_alt = alternativo
        datos.empleado = empl
        datos.observacion = detalle_uni
        datos.save()
         
        return redirect('generar_contrasenas')
            
    return redirect('generar_contrasenas')

def obtener_datos_correo_uni(request, id):
    try:
        datos = usuarioCorreos.objects.get(id_u_correo =id)
        if datos.correo_alt == None:
            dato_alias = 'Sin Alias'
        else:
            dato_alias = datos.correo_alt,
        data = {
            'correo_encontrado': datos.correo_usuario,
            'id_correo_uni' : datos.id_u_correo,

            'id_correo_alt_uni' : dato_alias,
        }
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)


 
def devolver_datos_uni(request, id):
    try:
 
        datos = usuarioCorreos.objects.get(id_u_correo=id)
 
        nombre = datos.asignado.empleado.first_name+' '+datos.asignado.empleado.last_name
        data = {
            'correo_alt': datos.correo_alt,
            'correo_usuario' : datos.correo_usuario,
            'empleado': nombre,
            'empleado_id': datos.asignado.empleado.id,
            'id_correo_devolver': id,
            
        }
    
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    



def devolver_datos_multi(request, id):
    try:
        datos = AsignacionCorreosUsuarios.objects.filter(correo=id).last()
        asignados = AsignacionCorreosUsuarios.objects.filter(correo=id)
        
        response_data = []
        for asignado in asignados:
            response_data.append({
                'empleado_id': asignado.empleado.id,
                'empleado_nombre': asignado.empleado.last_name, 
            })
        return render(request, 'cuentas/generar_contrasenas.html', {
            'correo_alt': datos.correo_alt,
            'correo_usuario': datos.correo.correo_usuario,
            'asignados': response_data  
        })

    except AsignacionCorreosUsuarios.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)

def completar_devolucion(request):
    if request.method == 'POST':
        id_correo = request.POST.get('devolver_id_correo_uni')
        obs = request.POST.get('devolver_detalle_uni')
        empleado = request.POST.get('empleado_devolver_uni')
        id_empleado = request.POST.get('empleadoid_devolver_uni')
        correo = usuarioCorreos.objects.get(id_u_correo = id_correo)
        asi = correo.asignado.id_asignacion
        datos_aux = AsignacionCorreosUsuarios.objects.get(id_asignacion = asi)
        datos_aux.estado = False
        datos_aux.save()
        cambio =  BajaCorreosUsuarios()
        cambio.correo = correo.correo_usuario
        cambio.correo_alt = correo.correo_alt
        cambio.fecha =  timezone.now()
        cambio.observacion = obs
        cambio.empleado = request.user
        cambio.save()
        
        correo.asignado.baja = cambio
        correo.asignado = None
        correo.estado = 0
        correo.save()

        # obtener= DatosPersonal.objects.get(empleado_id=id_empleado)
        # print('DEBUG OBTENIDO')
        # print(obtener)
        # contrato = Empleo.objects.get(empleado_id = obtener.id_datos)
        # print('DEBUG OBTENIDO')
        # print(contrato)
        # contrato.correo_corp = None
        
        # contrato.save()

        
        return redirect('generar_contrasenas') 
    

def password_equipos(request):
    datos = EquiposCuentas.objects.all()
    equipos = Equipos.objects.filter(activo = True)
    
    usuarios = User.objects.filter(is_active = True).order_by('first_name')
    tipos = TipoContrasenaEquipos.objects.all()
    motivos = MotivoCambio.objects.all()
    return render(request, 'cuentas/equipos_perifericos.html', {'datos':datos, 'usuarios':usuarios, 'equipos': equipos, 'tipos':tipos , 'motivos':motivos})
   

def verificar_codigo_equipo(request):
    if request.method == "POST":
        codigo_ingresado = request.POST.get('codigo_ingresado')
        data_id = request.POST.get('data') 
        registro = EquiposCuentas.objects.filter(id_cuenta_equipo = data_id).last()
        equipo = registro.asignado_id.id_cuenta_equipo
       
        registro2 = AsignadoEquipoCuenta.objects.filter( id_cuenta_equipo = equipo).last()
        clave_guardada = base64.urlsafe_b64decode(registro2.clave.encode('utf-8')) 
        f = Fernet(clave_guardada)
        
        asunto_cifrado = base64.urlsafe_b64decode(registro.datos.encode('utf-8'))
        mensaje_desencriptado = f.decrypt(asunto_cifrado).decode('utf-8')
      
        verificacion = VerificacionCodigo.objects.last()
        if verificacion and verificacion.codigo == codigo_ingresado:
            tiempo_restante = (now() - verificacion.tiempo_expiracion).seconds
            if tiempo_restante <= 180:  
                return JsonResponse({
                    'success': True,
                    'codigo': mensaje_desencriptado,
                    'message': 'Código verificado correctamente'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'El código ha expirado'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Código incorrecto'
            })

    return redirect('credencial')  


def agregar_usuario_equipo(request):
    if request.method == 'POST':
        equipo = request.POST.get('equipo_seleccionado')
        fecha = request.POST.get('fecha_asignado_equipo')
        tipo = request.POST.get('tipo_equipo_cuenta')
        contrasena = request.POST.get('contrasena')
        usuario =  request.POST.get('usuario_equipo')
        observaciones = request.POST.get('observaciones')

        empleado = request.POST.get('select_empleado_1')
        empelado_clase = User.objects.get(id=empleado)
        clave = Fernet.generate_key()
       
        mensaje = contrasena.encode()
        f = Fernet(clave)
        encriptado = f.encrypt(mensaje)
        asunto = base64.urlsafe_b64encode(encriptado).decode('utf-8')
        marca = base64.urlsafe_b64encode(clave).decode('utf-8')


        clase_equipo = Equipos.objects.get(id_equipo = equipo)
        
        empl = AsignadoEquipoCuenta()
        empl.codigo_equipo =  clase_equipo.codigo_equipo
        empl.fecha_cambio  = timezone.now()
        empl.estado = 2
        empl.clave = marca
        empl.usuario = empelado_clase
        empl.save()

        nuevo = EquiposCuentas()
        
        nuevo.equipo_id = clase_equipo
        nuevo.fecha = fecha
        tipo_clase = TipoContrasenaEquipos.objects.get(id_tipo = tipo)
        nuevo.tipo = tipo_clase
        nuevo.observaciones = observaciones
        nuevo.usuario_cuenta = usuario
        nuevo.encargado =  request.user
        nuevo.asignado_id = empl
        nuevo.datos = asunto
        nuevo.save()

        control = controlUsuario()
        control.fecha = timezone.now()
        control.detalle = 'creacion de usuario a cuenta de equipo' + empl.codigo_equipo
        control.usuario = request.user
        control.tipo = 2
        control.save()

    return redirect(password_equipos)


def info_equipos_cuentas_editar(request, id_datos):
    try:
       
        datos_editar = EquiposCuentas.objects.get(id_cuenta_equipo=id_datos)
        data = {
             
            'equipo_id': datos_editar.equipo_id.id_equipo,
            'observaciones': datos_editar.observaciones,
            'datos': datos_editar.datos,
            'tipo': datos_editar.tipo.id_tipo,
            'id': datos_editar.id_cuenta_equipo,
            'asignado_id': datos_editar.asignado_id.id_cuenta_equipo,
            'fecha': datos_editar.fecha.strftime('%Y-%m-%d'),
            'usuario_cuenta': datos_editar.usuario_cuenta,
        }

      
        return JsonResponse(data)
    except EquiposCuentas.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    


def editar_usuario_equipo(request):
    if request.method == 'POST':
        equipo = request.POST.get('equipo_seleccionado_editar')
        fecha = request.POST.get('fecha_asignado_equipo_editar')
        tipo = request.POST.get('tipo_equipo_cuenta_editar')
        id = request.POST.get('id_usuario_equipo')
        usuario =  request.POST.get('usuario_equipo_editar')
        observaciones = request.POST.get('observaciones_editar')

        editar = EquiposCuentas.objects.get(id_cuenta_equipo = id)
        clase_equipo = Equipos.objects.get(id_equipo = equipo)
        editar.equipo_id = clase_equipo
        editar.fecha = fecha
        tipo_clase = TipoContrasenaEquipos.objects.get(id_tipo = tipo)
        editar.tipo = tipo_clase
        editar.observaciones = observaciones
       
        editar.encargado =  request.user
        editar.save()

    return redirect(password_equipos)




def info_cambiar(request, id_datos):
    try:
       
        datos_editar = EquiposCuentas.objects.get(id_cuenta_equipo=id_datos)
        data = {
             
            'equipo_cambio': datos_editar.equipo_id.nombre,
            'id_equipo_cambio': id_datos,
        }

   
 
        return JsonResponse(data)
    except EquiposCuentas.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def cambiar_contrasena_cuenta(request):
    if request.method == 'POST':
        equipo = request.POST.get('equipo_cambio')
        id = request.POST.get('id_caso')
        tipo = request.POST.get('tipo_cambiar')
        estado = request.POST.get('cambiar_estado')
        empleado = request.POST.get('cambiar_empleado')
         
        contrasena = request.POST.get('cambiar_contrasena_cuenta')
        actualizar = EquiposCuentas.objects.get(id_cuenta_equipo=id)
        tipo_clase = MotivoCambio.objects.get(id_motivo = tipo)
        actualizar.motivo = tipo_clase
        actualizar.fecha = timezone.now()
        id_asignado = actualizar.asignado_id.id_cuenta_equipo
        asignados = AsignadoEquipoCuenta.objects.get(id_cuenta_equipo = id_asignado)
        if contrasena:
            clave = Fernet.generate_key()
            mensaje = contrasena.encode()
            f = Fernet(clave)
            encriptado = f.encrypt(mensaje)
            asunto = base64.urlsafe_b64encode(encriptado).decode('utf-8')
            marca = base64.urlsafe_b64encode(clave).decode('utf-8')
            actualizar.datos = asunto
            asignados.clave = marca

        if empleado :
            empleado_clase = User.objects.get(id = empleado)
            asignados.usuario = empleado_clase
        
            
        actualizar.save()
        asignados.save()

        control = controlUsuario()
        control.fecha = timezone.now()
        control.detalle = 'cambio de informacion de equipo' + equipo
        control.usuario = request.user
        control.tipo = 2
        control.save()


    return redirect(password_equipos)




def info_cuenta_editar(request, id_datos):
    try:
       
        datos_editar = usuarioCorreos.objects.get(id_u_correo=id_datos)
        data = {
             
            'id_u_correo': datos_editar.id_u_correo,
            'correo_usuario': datos_editar.correo_usuario,
            
            'compartido': datos_editar.compartido,
            'tipo': datos_editar.tipo,
            'observacion': datos_editar.observacion,
            'fecha': datos_editar.fecha.strftime('%Y-%m-%d'),
            
        }

       
        return JsonResponse(data)
    except usuarioCorreos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    


def editar_cuenta_correo(request):
    if request.method == 'POST':
        id = request.POST.get('id_editar')
        correo = request.POST.get('correo_editar')
        tipo = request.POST.get('tipo_editar')
        compartir = request.POST.get('alias_correo_editar')
        obs = request.POST.get('observaciones_editar')
        fecha = request.POST.get('fecha_asignado_editar')
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    
        cuenta = usuarioCorreos.objects.get(id_u_correo=id)
        cuenta.correo_usuario = correo
        cuenta.tipo = tipo
        cuenta.compartido = compartir
        cuenta.observacion = obs
        cuenta.fecha = fecha
      
        cuenta.save()  

    return redirect('generar_contrasenas')



def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
    try:
        print(f"[DEBUG] Comprobando la existencia de la carpeta '{carpeta_nombre}'")
        query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
        if carpeta_padre_id:
            query += f" and '{carpeta_padre_id}' in parents"
        
        service = authenticate_google_drive()
        resultados = service.files().list(q=query, fields="files(id, name)").execute()
        folders = resultados.get('files', [])
        print(f"[DEBUG] Carpeta(s) encontrada(s): {folders}")

        if folders:
            return folders[0]['id']
        else:
            file_metadata = {
                'name': carpeta_nombre,
                'mimeType': 'application/vnd.google-apps.folder',
            }
            if carpeta_padre_id:
                file_metadata['parents'] = [carpeta_padre_id]

            carpeta = service.files().create(body=file_metadata, fields='id').execute()
            print(f"[DEBUG] Carpeta '{carpeta_nombre}' creada con ID: {carpeta['id']}")
            return carpeta['id']
    except Exception as e:
        print(f"[ERROR] Error al obtener o crear la carpeta: {str(e)}")
        raise Exception(f"Error al obtener o crear la carpeta en Drive: {str(e)}")

 

def guardar_imagen_drive(image_data, image_filename):
    try:
        image_file = base64.b64decode(image_data)
        temp_file_path = os.path.join(settings.MEDIA_ROOT, image_filename)
        with open(temp_file_path, 'wb') as f:
            f.write(image_file)
        service = authenticate_google_drive()
        carpeta_documentos_id = obtener_o_crear_carpeta('VILASECA - SOPORTE TECNICO')
        file_metadata = {
            'name': image_filename,
            'parents': [carpeta_documentos_id]
        }
        media = MediaFileUpload(temp_file_path, mimetype='image/jpeg')
        file_drive = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"
        def eliminar_archivo():
            try:
                os.remove(temp_file_path)  
            except Exception as e:
                print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")
        
        Timer(300, eliminar_archivo).start() 

        return ruta_final  

    except Exception as e:
        raise Exception(f"Error al procesar la imagen: {str(e)}")


def guardar_mensaje(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            contenido_limpio = re.sub(r'<[^>]+>', '', content)
            if 'data:image' in content:
                start = content.find('base64,') + len('base64,')
                end = len(content)
                image_data = content[start:end]
                
                fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_filename = f"imagen_{fecha_actual}.jpg"
                try:
                    image_url = guardar_imagen_drive(image_data, image_filename)
                    imagen_incluida = f'<a href="{image_url}">{image_url}</a>'
                    contenido_limpio = contenido_limpio.replace('data:image/jpeg;base64,', 'Con Imagen Adjunto')
                    content = content.replace(f'data:image/jpeg;base64,{image_data}', imagen_incluida)
                except Exception as e:
                    return JsonResponse({'error': f'Error al procesar la imagen: {str(e)}'})
          
                nueva_auditoria = SolicitudServicioTecnico(
                    fecha=timezone.now(),
                    
                    codigo = f"VLSC-TICKET-{timezone.now()}",
                    usuario=request.user,
                    mensaje=contenido_limpio,  
                    foto=image_url  
                )
            else:
                nueva_auditoria = SolicitudServicioTecnico(
                    fecha=timezone.now(),
                    
                    codigo = f"VLSC-TICKET-{timezone.now()}",
                    usuario=request.user,
                    mensaje=contenido_limpio,  
                    
                )
            
            nueva_auditoria.save()
            
            asunto = "Nuevo mensaje de servicio técnico"
            mensaje_html = f"<div style='text-align: center; padding:50px;'>{content}</div>"
            destinatario = settings.BASE_CORREO
         
            send_mail(
                asunto,
                '',
                settings.DEFAULT_FROM_EMAIL,   
                [destinatario],   
                html_message=mensaje_html,   
            )
            total_soporte = SolicitudServicioTecnico.objects.filter(estado=False).count()
            request.session['total_soporte'] = total_soporte
            ultimos_soportes = SolicitudServicioTecnico.objects.filter(estado=False).order_by('-id_ticket')[:3]
            
            soportes_info = {}
            
            for i, soporte in enumerate(ultimos_soportes):
                soportes_info[f"soporte_{i+1}_id"]  = soporte.id_ticket  
                soportes_info[f"soporte_{i+1}_mensaje"] = soporte.mensaje  
                soportes_info[f"soporte_{i+1}_nombre"] = soporte.usuario.first_name+' '+soporte.usuario.last_name  
            
            request.session['soportes_info'] = soportes_info
        
            return JsonResponse({'message': 'Mensaje guardado y enviado por correo exitosamente'})

    except Exception as e:
        return JsonResponse({'error': f'Error al guardar el mensaje: {str(e)}'})

def soporte_tecnico(request):
     
    datos = SolicitudServicioTecnico.objects.filter(estado= False).order_by('-id_ticket')

    total_soporte = SolicitudServicioTecnico.objects.filter(estado=False).count()
    request.session['total_soporte'] = total_soporte
    ultimos_soportes = SolicitudServicioTecnico.objects.filter(estado=False).order_by('-id_ticket')[:3]
    
    soportes_info = {}
    
    for i, soporte in enumerate(ultimos_soportes):
        soportes_info[f"soporte_{i+1}_id"]  = soporte.id_ticket  
        soportes_info[f"soporte_{i+1}_mensaje"] = soporte.mensaje  
        soportes_info[f"soporte_{i+1}_nombre"] = soporte.usuario.first_name+' '+soporte.usuario.last_name  
    
    request.session['soportes_info'] = soportes_info
    return render(request, 'soporte/t_solicitudes.html', {'datos':datos})

 
def obtener_tickets(request):
    datos = SolicitudServicioTecnico.objects.filter(estado=False)
    response_data = []

    for dato in datos:
        response_data.append({
            'id_ticket': dato.id,
            'fecha': dato.fecha,
            'mensaje': dato.mensaje,
            'foto': dato.foto.url if dato.foto else None,
            'estado': 'En Revisión' if not dato.estado else 'Completado',
            'usuario': dato.usuario.first_name + ' ' + dato.usuario.last_name,
        })

    return JsonResponse({'datos': response_data})


def info_ticket(request, id_datos):
    try:
        ticket = SolicitudServicioTecnico.objects.get(id_ticket=id_datos)
        empleado_id = ticket.usuario.id  
        equipo = Equipos.objects.filter(estado=True, asignacion__empleado=empleado_id)
        cuenta = AsignacionCorreosUsuarios.objects.filter(estado=True, empleado=empleado_id)
        equipos_list = [f"{e.codigo_equipo} - {e.nombre}" for e in equipo]  
        cuentas_list = [f"{c.correo} - {c.correo_alt}" for c in cuenta]
        sistema = CuentasSoftwares.objects.filter(asignado__empleado=empleado_id)
        periferico = EquiposCuentas.objects.filter(asignado_id__usuario=empleado_id)

        sis_list = [f"{s.usuario} - {s.sistema.nombre}" for s in sistema]  
        periferico_list = [f"{p.usuario_cuenta} - {p.equipo_id.nombre}" for p in periferico]  
        nombre_empleado = ticket.usuario.first_name+' '+ticket.usuario.last_name
        return JsonResponse({
            'empleado': nombre_empleado,  
            'equipos': equipos_list,
            'perifericos': periferico_list,
            'sistemas': sis_list,
            'cuentas': cuentas_list
        })
        
    except SolicitudServicioTecnico.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)

def solucion_tickets(request):
    datos = SolicitudServicioTecnico.objects.filter(estado= True)
    return render(request, 'soporte/t_solucionados.html', {'datos':datos})


def completar_ticket(request):
    if request.method == 'POST':
        id = request.POST.get('ids')
        diagnostico = request.POST.get('diagnostico')
        accion = request.POST.get('accion')
        correccion = request.POST.get('correccion')
        recomendacion = request.POST.get('recomendacion')
        observacion = request.POST.get('observacion')
        fecha = timezone.now()
        solicitud = SolicitudServicioTecnico.objects.get(id_ticket=id)
        solicitud.diagnostico = diagnostico
        solicitud.accion = accion
        solicitud.correccion = correccion
        solicitud.recomendacion = recomendacion
        solicitud.observacion = observacion
        solicitud.fecha_respuesta = fecha
        solicitud.estado = True
        solicitud.save()  
        total_soporte = SolicitudServicioTecnico.objects.filter(estado=False).count()
        request.session['total_soporte'] = total_soporte
        ultimos_soportes = SolicitudServicioTecnico.objects.filter(estado=False).order_by('-id_ticket')[:3]
    
        soportes_info = {}
        
        for i, soporte in enumerate(ultimos_soportes):
            soportes_info[f"soporte_{i+1}_id"]  = soporte.id_ticket  
            soportes_info[f"soporte_{i+1}_mensaje"] = soporte.mensaje  
            soportes_info[f"soporte_{i+1}_nombre"] = soporte.usuario.first_name+' '+soporte.usuario.last_name  
        
        request.session['soportes_info'] = soportes_info
        print(soportes_info)

    return redirect('solucion_tickets')

def eliminar_usuario(request):
    if request.method == 'POST':
        try: 
            id = request.POST.get('id_eliminar')
            actualizar = User.objects.get(id=id)
            actualizar.is_active = False
            actualizar.save()
            return redirect(f"{reverse('empleados')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('empleados')}?error=true")
  
    return redirect("empleados")

def activar_usuario(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = User.objects.get(id=id)
            actualizar.is_active = True
            actualizar.save()
            return redirect(f"{reverse('empleados')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('empleados')}?error=true")
  
    return redirect("empleados")

def agregar_datos_contrato(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('codigo')
            fecha = request.POST.get('fecha_registro_crear')
            inicio = request.POST.get('inicio_contrato_crear')
            modalidad = request.POST.get('modalidad_crear')
            celular_crear = request.POST.get('celular_crear')
            whatsapp_crear = request.POST.get('whatsapp_crear')
            interno_crear = request.POST.get('interno_crear')
            tipo = request.POST.get('tipo_registro_crear')
            tipo2 = request.POST.get('tipo_contrato_crear')
            trabajo_centro = request.POST.get('trabajo_centro')
            cargo = request.POST.get('cargoarea')
            nuevo = Empleo()
            marca = DatosPersonal.objects.get(empleado_id=id)
            nuevo.empleado_id = marca
            
            nuevo.fecha_registro =timezone.now()
            nuevo.inicio_contrato = inicio
            nuevo.modalidad = modalidad
            nuevo.numero_trabajo = celular_crear
            nuevo.whatsapp = whatsapp_crear
            nuevo.nro_interno = interno_crear
            regi = TipoContrato.objects.get(id_contrato=tipo2)
            regi2 = TipoRegistro.objects.get(id_registro = tipo)
            nuevo.tipo_registro = regi2
            marcacargo = AreasCargos.objects.get(id_area = cargo)
            nuevo.clasificacion = marcacargo
            nuevo.tipo_contrato = regi
            marca = Oficina.objects.get(id_oficina = trabajo_centro)
            nuevo.centro_trabajo = marca
            nuevo.save()

            return redirect(f"{reverse(datos_contratos)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(datos_contratos)}?error=true")
    
    return redirect(datos_contratos)   

 
def eliminar_equipo(request):
    if request.method == 'POST':
        id = request.POST.get('id_eliminar')
        actualizar = Equipos.objects.get(id_equipo=id)
        actualizar.activo = False
        actualizar.save()
    return redirect('listar_equipos')

def activar_equipo(request):
    if request.method == 'POST':
        id = request.POST.get('id_activar')
        actualizar = Equipos.objects.get(id_equipo=id)
        actualizar.activo = True
        actualizar.save()
    return redirect('listar_equipos')

def sistemas(request):
    datos = Softwares.objects.all()
    return render(request, 'equipos/softwares.html', {'datos': datos})

def agregar_sistema_software(request):
    if request.method == 'POST':
        nombre_sistema = request.POST.get('nombre_sistema')
        puerto = request.POST.get('puerto')
        ip = request.POST.get('ip')
        enlace = request.POST.get('enlace')
        descripcion = request.POST.get('descripcion')
        nuevo = Softwares()
        nuevo.nombre = nombre_sistema
        nuevo.ip = ip
        nuevo.enlace = enlace
        nuevo.fecha = timezone.now()
        nuevo.puerto = puerto
        nuevo.descripcion = descripcion
        nuevo.save()
        return redirect(sistemas)


def info_software_editar(request, id_datos):
    try:
        sistema = Softwares.objects.get(id_sistema =id_datos)

        
        return JsonResponse({
            'id_sistema' : sistema.id_sistema,
            'enlace' : sistema.enlace,
            'ip' : sistema.ip,
            'puerto' : sistema.puerto,
            'descripcion' : sistema.descripcion,
            'nombre': sistema.nombre,
        })
        
    except Softwares.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)


def eliminar_software(request):
    if request.method == 'POST':
        id = request.POST.get('id_eliminar')
        actualizar = Softwares.objects.get(id_sistema=id)
        actualizar.activo = False
        actualizar.save()
    return redirect('sistemas')

def activar_software(request):
    if request.method == 'POST':
        id = request.POST.get('id_activar')
        actualizar = Softwares.objects.get(id_sistema=id)
        actualizar.activo = True
        actualizar.save()
    return redirect('sistemas')


def editar_sistema_software(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_sistema_editar')
        id_sistema = request.POST.get('id_sistema')
        ip_editar = request.POST.get('ip_editar')
        puerto_editar = request.POST.get('puerto_editar')
        enlace_editar = request.POST.get('enlace_editar')
        descripcion = request.POST.get('descripcion')
        editar = Softwares.objects.get(id_sistema = id_sistema)
        editar.nombre = nombre
        editar.ip = ip_editar
        editar.puerto = puerto_editar
        editar.enlace = enlace_editar
        editar.fecha = timezone.now()
        editar.descripcion = descripcion
        editar.save()

    return redirect(sistemas)


def cuentas_sistemas(request):
    datos = CuentasSoftwares.objects.all()
    usuarios = User.objects.filter(is_active = True)
    sistemas = Softwares.objects.filter(activo = True)
    return render(request, 'cuentas/cuentas_sistemas.html', {'datos': datos, 'usuarios':usuarios, 'sistemas':sistemas})

def agregar_cuenta_software(request):
    if request.method == 'POST':
        nombre_sistema = request.POST.get('nombre_sistema')
        fecha = request.POST.get('fecha')
        usuario_cuenta = request.POST.get('usuario_cuenta')
        tipo_cuenta = request.POST.get('tipo_cuenta')
        empleado = request.POST.get('empleado')
        observaciones = request.POST.get('observaciones')
        nuevo = CuentasSoftwares()
        nuevo.usuario = usuario_cuenta
        nuevo.fecha = fecha
        nuevo.tipo_usuario = tipo_cuenta
        nuevo.fecha = timezone.now()
        marca = Softwares.objects.get(id_sistema = nombre_sistema)
        nuevo.sistema = marca
        nuevo.observaciones = observaciones
        nuevo.estado = True
        asignado = AsignarCuentasSoftwares()
        asignado.fecha = timezone.now()
        asignado.usuario = usuario_cuenta
        aux = User.objects.get(id = empleado)
        asignado.empleado = aux
        asignado.save()
        nuevo.asignado = asignado
        nuevo.save()

        return redirect(cuentas_sistemas)

def eliminar_cuentas_software(request):
    if request.method == 'POST':
        id = request.POST.get('id_eliminar')
        actualizar = CuentasSoftwares.objects.get(id_cuenta=id)
        actualizar.activo = False
        actualizar.save()
    return redirect('cuentas_sistemas')

def activar_cuentas_software(request):
    if request.method == 'POST':
        id = request.POST.get('id_activar')
        actualizar = CuentasSoftwares.objects.get(id_cuenta=id)
        actualizar.activo = True
        actualizar.save()
    return redirect('cuentas_sistemas')




def info_cuenta_software_editar(request, id_datos):
    
    try:
        sistema = CuentasSoftwares.objects.get(id_cuenta =id_datos)
       
        return JsonResponse({
            'id_cuenta' : sistema.id_cuenta,
            'fecha' : sistema.fecha.strftime('%Y-%m-%d'),
            'usuario' : sistema.usuario,
            'tipo_usuario' : sistema.tipo_usuario,
            'observaciones' : sistema.observaciones,
            'sistema': sistema.sistema.id_sistema,
           
        })
    
    except CuentasSoftwares.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)


def info_cuenta_software_devolver(request, id_datos):
    
    try:
        sistema = CuentasSoftwares.objects.get(id_cuenta =id_datos)
        asignado = sistema.asignado
        nombre = sistema.asignado.empleado.first_name+' '+sistema.asignado.empleado.last_name
        print(nombre)
        return JsonResponse({
    
            'usuario_devolver' : sistema.usuario,
            'id_cuenta' : id_datos,
             
            'sistema_devolver': sistema.sistema.nombre,
            'asignado_devolver': sistema.asignado.empleado.id,
            'asignado_devolver_nombre': nombre,
        })
    
    except CuentasSoftwares.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrada'}, status=404)


def devolver_cuenta_sistemas(request):
    if request.method == 'POST':
        sistema_devolver = request.POST.get('sistema_devolver')
        usuario_devolver = request.POST.get('usuario_devolver')
        empleado_devolver_nombre = request.POST.get('empleado_devolver_nombre')
        id_devolver = request.POST.get('id_devolver')
        observacion_devolver = request.POST.get('observacion_devolver')
        

        actualizar = CuentasSoftwares.objects.get(id_cuenta=id_devolver)
        dato= actualizar.asignado.id_asignado
        asignados = AsignarCuentasSoftwares.objects.get(id_asignado = dato)

        baja = BajaCuentasSoftwares()
        baja.fecha = timezone.now()
        baja.usuario = asignados.usuario
        baja.observacion = observacion_devolver
        baja.usuario_baja = request.user
        baja.save()

        asignados.baja = baja
        asignados.save()
        actualizar.asignado = None
        actualizar.estado = False
        actualizar.save()

    return redirect('cuentas_sistemas')
 

def asignar_cuenta_sistemas(request):
    if request.method == 'POST':
        id_asignar = request.POST.get('id_asignar')
        usuario_asig = request.POST.get('usuario_asig')
        fecha_asig = request.POST.get('fecha_asig')
        empleado_asig = request.POST.get('empleado_asig')
        observacion_asig = request.POST.get('observacion_asig')
        asignados = AsignarCuentasSoftwares()
        asignados.fecha = fecha_asig
        asignados.usuario = usuario_asig
        asignados.observacion = observacion_asig
        marca = User.objects.get(id = empleado_asig)
        asignados.empleado = marca
        asignados.save()
        actualizar = CuentasSoftwares.objects.get(id_cuenta=id_asignar)
        actualizar.asignado = asignados
        actualizar.estado = True
        actualizar.save()

    return redirect('cuentas_sistemas')

def cuenta_teletrabajo(request):
    datos = CuentasTeletrabajo.objects.all()
    usuarios = User.objects.filter(is_active = True)
    equipos = Equipos.objects.filter(activo = True)
    return render(request, 'cuentas/teletrabajo.html', {'datos': datos, 'usuarios':usuarios, 'equipos':equipos})



def agregar_cuenta_teletrabajo(request):
    if request.method == 'POST':
        
        try:
            nombre_equipo = request.POST.get('nombre_equipo')
            fecha = request.POST.get('fecha')
            ip_teletrabajo = request.POST.get('ip_teletrabajo')
            tipo_acceso = request.POST.get('tipo_acceso')
            empleado = request.POST.get('empleado')
            firmware = request.POST.get('firmware')
            dst = request.POST.get('dst')
            observaciones = request.POST.get('observaciones')
            
            nuevo = CuentasTeletrabajo()
            nuevo.fecha = fecha
            nuevo.ip_equipo = ip_teletrabajo
            nuevo.tipo_acceso = tipo_acceso
            nuevo.firmware =firmware
            nuevo.dst = dst
            nuevo.observaciones = observaciones
            dato_empleado = User.objects.get(id = empleado)
            eq = Equipos.objects.get(id_equipo = nombre_equipo)
            nuevo.equipo = eq
            nuevo.estado = True
            asignacion = AsignarCuentaTeletrabajo()
            asignacion.fecha = fecha
            asignacion.empleado = dato_empleado
            asignacion.save()

            nuevo.asignado = asignacion
            nuevo.save()

            return redirect(f"{reverse('cuenta_teletrabajo')}?success=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")

    return redirect('cuenta_teletrabajo')

def eliminar_cuentas_teletrabajo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = CuentasTeletrabajo.objects.get(id_teletrabajo=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse('cuenta_teletrabajo')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")
    
    return redirect('cuenta_teletrabajo')

def activar_cuentas_teletrabajo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = CuentasTeletrabajo.objects.get(id_teletrabajo=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse('cuenta_teletrabajo')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")
    return redirect('cuenta_teletrabajo')


def asignar_cuenta_teletrabajo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_asignar')
            fecha = request.POST.get('fecha_asig')
            observacion_asig = request.POST.get('observacion_asig')
            empleado_asig = request.POST.get('empleado_asig')
            actualizar = CuentasTeletrabajo.objects.get(id_teletrabajo=id)
            
            asignar = AsignarCuentaTeletrabajo()
            asignar.equipo = actualizar.equipo 
            asignar.ip_equipo =  actualizar.ip_equipo
            asignar.tipo_acceso =  actualizar.tipo_acceso
            asignar.firmware =  actualizar.firmware
            asignar.dst =  actualizar.dst
            user = User.objects.get(id=empleado_asig)
            asignar.empleado = user
            asignar.fecha = fecha
            asignar.observaciones = observacion_asig
            asignar.save()
            actualizar.estado= True
            actualizar.asignado= asignar
            actualizar.save()
            return redirect(f"{reverse('cuenta_teletrabajo')}?asignar=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")

    return redirect('cuenta_teletrabajo')



def devolver_cuenta_teletrabajo(request):
    if request.method == 'POST':
        try:
            id_devolver = request.POST.get('id_devolver')
            obs = request.POST.get('observacion_devolver')
            actualizar = CuentasTeletrabajo.objects.get(id_teletrabajo=id_devolver)
            data = actualizar.asignado.id_asignado
            asignar = AsignarCuentaTeletrabajo.objects.get(id_asignado = data)
            devol = BajaCuentaTeletrabajo()
            devol.fecha = timezone.now()
            devol.usuario = request.user
            devol.observaciones = obs
            devol.save()
            asignar.baja = devol
            actualizar.asignado = None
            actualizar.estado = False
            actualizar.save()
            asignar.save()
            return redirect(f"{reverse('cuenta_teletrabajo')}?devolver=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")
    return redirect('cuenta_teletrabajo')
    


def info_teletrabajo(request, id_datos):
    try:
        datos_editar = CuentasTeletrabajo.objects.get(id_teletrabajo=id_datos)
       
        data = {
          
            'ip_teletrabajo_editar' : datos_editar.ip_equipo, 
            'fecha_editar' : datos_editar.fecha.strftime('%Y-%m-%d'),
            'nombre_equipo_editar' : datos_editar.equipo.id_equipo,
            'tipo_acceso_editar' : datos_editar.tipo_acceso,
            'observaciones_editar' : datos_editar.observaciones,
            'dst_editar' : datos_editar.dst,
            'firmware_editar' : datos_editar.firmware,
            'id_tele': datos_editar.id_teletrabajo,
            
        }
        
        return JsonResponse(data)
    except Equipos.DoesNotExist:
        return JsonResponse({'error': 'Persona no encontrado'}, status=404)
    
def listar_backups(request):
    datos = EstadoBackups.objects.all()

    return render(request, 'backups/listar_backups.html',{'datos':datos})


def agregar_informe_backup(request):
    if request.method == 'POST':
        try:
            doc = request.FILES.get('subir_informe') 
            data_total_toma = request.POST.get('data_total_toma')
            print('[DEBUG]')
            print(data_total_toma)
            id_backup = request.POST.get('id_backup')
            try:
                nuevo = EstadoBackups.objects.get(id_estado_b=id_backup)
            except EstadoBackups.DoesNotExist:
                return redirect(listar_backups)
            nuevo.estado = 1 if int(data_total_toma) <= 4 else 0

            def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
                query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
                if carpeta_padre_id:
                    query += f" and '{carpeta_padre_id}' in parents"
                resultados = service.files().list(q=query, fields="files(id, name)").execute()
                folders = resultados.get('files', [])

                if folders:
                    return folders[0]['id']
                else:
                    file_metadata = {
                        'name': carpeta_nombre,
                        'mimeType': 'application/vnd.google-apps.folder',
                    }
                    if carpeta_padre_id:
                        file_metadata['parents'] = [carpeta_padre_id]

                    carpeta = service.files().create(body=file_metadata, fields='id').execute()
                    print(f"[DEBUG] Carpeta '{carpeta_nombre}' creada con ID: {carpeta['id']}")
                    return carpeta['id']
            service = authenticate_google_drive()
            carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA VILASECA MODULO BACKUPS')
            carpeta_empleado_id = obtener_o_crear_carpeta('INFORMES', carpeta_padre_id=carpeta_documentos_id)
            nombre = nuevo.equipo.codigo_equipo
            fecha_actual = timezone.now()
            archivo_guardado_nombre = f"{nombre}_{fecha_actual.strftime('%Y%m%d_%H%M%S')}"
            temp_file_path = os.path.join(settings.MEDIA_ROOT, archivo_guardado_nombre)
            with open(temp_file_path, 'wb') as f:
                for chunk in doc.chunks(): 
                    f.write(chunk)
            file_metadata = {
                'name': archivo_guardado_nombre,
                'parents': [carpeta_empleado_id]
            }
            media = MediaFileUpload(temp_file_path, mimetype=doc.content_type)
            file_drive = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"[DEBUG] Archivo subido a Google Drive con ID: {file_drive['id']}")
            ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"
            def eliminar_archivo():
                try:
                    os.remove(temp_file_path)
                    print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")
            Timer(300, eliminar_archivo).start()
            nuevo.informe_drive = ruta_final
            nuevo.fecha = timezone.now()
            nuevo.usuario = request.user
            nuevo.save()
            return redirect(f"{reverse('listar_backups')}?success=true")

        except Exception as e:
            return redirect(f"{reverse('listar_backups')}?error=true")

    return redirect(listar_backups)

def registro_backups(request):
    datos = Backups.objects.all()
    equipos = Equipos.objects.filter(activo = True)
    usuarios = User.objects.filter(is_active = True).order_by('first_name')
    discos = DiscoBackups.objects.all()
    return render(request, 'backups/registro_backups.html',{'datos':datos, 'equipos':equipos, 'usuarios':usuarios, 'discos':discos})





def registro_backups_nuevo(request):
    if request.method == 'POST':
        try:
            gestion = request.POST.get('gestion')
            fecha = request.POST.get('fecha_ejecucion')
            id = request.POST.get('equipo_verificar')
            periodo = request.POST.get('periodo')
            id_emplea = request.POST.get('empleado_verificar')
            obs = request.POST.get('observaciones')
            tipo_nuevo = request.POST.get('tipo_nuevo')
 
            marcas = User.objects.get(id=id_emplea)
            nuevo = Backups()
            nuevo.fecha = fecha
            nuevo.gestion = gestion
            marca = Equipos.objects.get(id_equipo=id)
            nuevo.equipo = marca
            nuevo.usuario = marcas
            nuevo.periodo = periodo
            nuevo.observaciones = obs
            nuevo.tipo_backup = tipo_nuevo
            marca_estado = EstadoBackups.objects.filter(equipo=id).last()
            verificado = VerificacionBackups()
            verificado.fecha = timezone.now()
            verificado.gestion = gestion
            verificado.obs = 'No Verificado'
            verificado.save()
            nuevo.verificar = verificado
            if marca_estado is None:
                nuevo.estado = None
            else:
                nuevo.estado = marca_estado

            nuevo.save()
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
          
            evento = Calendario()
            evento.title = f"Backup del EQUIPO  {marca.codigo_equipo}"
            evento.descripcion = f"Backup del equipo: {marca.nombre} por motivo de '{tipo_nuevo}' a cargo de: {marcas.first_name} {marcas.last_name}"
            evento.start = (fecha + timedelta(hours=12)).isoformat()
            evento.end = (fecha + timedelta(hours=15)).isoformat()
            evento.color = '#9c9c9c'
            evento.save()


            return redirect(f"{reverse('registro_backups')}?success=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse('registro_backups')}?error=true")
    
    return redirect('registro_backups')



def editar_cuenta_software(request):
    if request.method ==  'POST':
        sistema =  request.POST.get('nombre_editar')
        id = request.POST.get('id_editar')
        
        fecha_editar = request.POST.get('fecha_editar')
        usuario_cuenta_editar = request.POST.get('usuario_cuenta_editar')
        tipo_cuenta_editar = request.POST.get('tipo_cuenta_editar')

        observaciones_editar = request.POST.get('observaciones_editar')
        editar =  CuentasSoftwares.objects.get(id_cuenta = id)
        editar.fecha = fecha_editar
        editar.usuario = usuario_cuenta_editar
        editar.tipo_usuario = tipo_cuenta_editar
        editar.observaciones = observaciones_editar
        marca = Softwares.objects.get(id_sistema = sistema)
        editar.sistema = marca
        editar.save()


    return redirect(cuentas_sistemas)


def editar_cuenta_teletrabajo(request):
    if request.method ==  'POST':
        try: 
            sistema =  request.POST.get('nombre_equipo_editar')
            id = request.POST.get('id_tele')
            fecha_editar = request.POST.get('fecha_editar')
            ip_teletrabajo_editar = request.POST.get('ip_teletrabajo_editar')
            tipo_acceso_editar = request.POST.get('tipo_acceso_editar')
            firmware_editar = request.POST.get('firmware_editar')
            dst_editar = request.POST.get('dst_editar')
            observaciones_editar = request.POST.get('observaciones_editar')
            editar =  CuentasTeletrabajo.objects.get(id_teletrabajo = id)
            editar.fecha = fecha_editar
            editar.ip_equipo = ip_teletrabajo_editar
            editar.tipo_acceso = tipo_acceso_editar
            editar.firmware = firmware_editar
            editar.dst = dst_editar
            editar.observaciones = observaciones_editar
            marca = Equipos.objects.get(id_equipo = sistema)
            editar.equipo = marca
            editar.save()
            return redirect(f"{reverse('cuenta_teletrabajo')}?editar=true")

        except Exception as e:
            return redirect(f"{reverse('cuenta_teletrabajo')}?error=true")

    return redirect(cuenta_teletrabajo)


def editar_backup(request):
    if request.method == 'POST':
        gestion = request.POST.get('gestion')
        fecha = request.POST.get('fecha_ejecucion')
        id = request.POST.get('equipo_seleccionado')
        periodo = request.POST.get('periodo')
        nuevo = Backups()
        nuevo.fecha = fecha
        nuevo.gestion = gestion
        marca = Equipos.objects.get(id_equipo = id)
        nuevo.equipo = marca
        nuevo.usuario = request.user
        nuevo.periodo = periodo
        marca_estado = EstadoBackups.objects.filter(equipo = id).last()
        print(marca_estado)
        if marca_estado == None:
            nuevo.estado = None
        else:
            nuevo.estado = marca_estado

        nuevo.save()
        
        return redirect(registro_backups)


def eliminar_informe_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = EstadoBackups.objects.get(id_estado_b=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse('listar_backups')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('listar_backups')}?error=true")
    
    return redirect('listar_backups')

def activar_informe_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = EstadoBackups.objects.get(id_estado_b=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse('listar_backups')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('listar_backups')}?error=true")
    return redirect('listar_backups')

def verifica_backups(request):
    datos = VerificacionBackups.objects.all()
    equipos = Equipos.objects.all()
    discos = DiscoBackups.objects.all()
    usuarios = User.objects.filter(is_active = True)
    return render(request, 'backups/verificar.html', {'datos':datos, 'equipos':equipos, 'discos': discos, 'usuarios':usuarios})


def registro_backups_verificado(request):
    if request.method == 'POST':
        try:
            equipo_seleccionado = request.POST.get('verificar_equipo')
            marca = Equipos.objects.get(codigo_equipo = equipo_seleccionado)

            select_empleado_1 = request.POST.get('select_empleado_1')
            fecha_ejecucion = request.POST.get('fecha_ejecucion')
            observaciones = request.POST.get('observaciones')
            id_disco = request.POST.get('numero_disco')
            id_cuenta = request.POST.get('id_datos_verificar')
            gestion =  request.POST.get('gestion_verificar')

            editar = Backups.objects.get(id_backup = id_cuenta)
            buscar = editar.verificar.id_backup
            disco = DiscoBackups.objects.get(id_disco=id_disco)
            id_cambio=editar.estado.id_estado_b 
            datocambio = EstadoBackups.objects.get(id_estado_b = id_cambio)
            datocambio.estado = True
            datocambio.save()
            verificado = VerificacionBackups.objects.get(id_backup = buscar)
            verificado.gestion = gestion
            verificado.disco_duro = disco
            verificado.obs = observaciones
            verificado.fechar_verificacion = timezone.now()
            verificado.fecha = fecha_ejecucion
            usuario = User.objects.get(id = select_empleado_1)

            verificado.revisor_cambio = usuario
            verificado.save()
         
            return redirect(f"{reverse('registro_backups')}?asignar=true")

        except Exception as e:

            return redirect(f"{reverse('registro_backups')}?error=true")
    return redirect('registro_backups')



def editar_verificacion_backup(request):
    if request.method == 'POST':
        try:
        
            id_editar = request.POST.get('id_editar')
            equipo_seleccionado = request.POST.get('equipo_seleccionado_editar')
            select_empleado_1 = request.POST.get('responsable_editar')
            fecha_ejecucion = request.POST.get('fecha_ejecucion_editar')
            observaciones = request.POST.get('observaciones_editar')
            id_disco = request.POST.get('numero_disco_editar')
            gestion =  request.POST.get('gestion_editar')  
            nuevo = VerificacionBackups.objects.get(id_backup=id_editar)
            marca = DiscoBackups.objects.get(id_disco = id_disco)
            nuevo.disco_duro = marca 
            nuevo.gestion = gestion
            datos = Equipos.objects.get(id_equipo = equipo_seleccionado)
            nuevo.equipo = datos
            us = User.objects.get(id = select_empleado_1)
            
            nuevo.responsable = us
            nuevo.fecha = fecha_ejecucion
            nuevo.obs = observaciones
            nuevo.save()
            return redirect(f"{reverse('verifica_backups')}?editar=true")

        except Exception as e:

            return redirect(f"{reverse('verifica_backups')}?error=true")
    return redirect('verifica_backups')


def eliminar_verificacion_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = VerificacionBackups.objects.get(id_backup=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse('verifica_backups')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('verifica_backups')}?error=true")
    
    return redirect('verifica_backups')

def activar_verificacion_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = VerificacionBackups.objects.get(id_backup=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse('verifica_backups')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('verifica_backups')}?error=true")
    return redirect('verifica_backups')

  
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
def authenticate_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def get_storage_info(drive_service):
    about = drive_service.about().get(fields="storageQuota").execute()
    print("datos de empresa")
    print(about)
    total = int(about['storageQuota']['limit'])  
    used = int(about['storageQuota']['usage'])  
    remaining = total - used                     

    return {
        'total': total,
        'usado': used,
        'restante': remaining
    }

def storage_info(request):
    try:
        drive_service = authenticate_drive()  
        storage_data = get_storage_info(drive_service) 
        datos = []  

        for _ in range(1):
            datos.append({
                'correo': {
                    'correo_usuario': 'sistemas@agencia-vilaseca.com', 
                    'tipo': 'DOMINIO'
                },
                'fecha': '2025-02-13', 
                'total': storage_data['total'],
                'usado': storage_data['usado'],
                'restante': storage_data['restante'],
                'estado': 'Activo',  
                'id_backup_correos': '1',  
                'activo': 1  
            })
        return render(request, 'backups/verificar.html', {'datos': datos})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def backups_correos(request):
    datos = BackupsCorreos.objects.all()
    correos = usuarioCorreos.objects.exclude(asunto=None)
    discos = DiscoBackups.objects.all()
    usuarios = User.objects.filter(is_active = True)
    return render(request, 'backups/backup_correo.html', {'datos':datos, 'correos':correos, 'discos': discos, 'usuarios':usuarios})

def agregar_backup_correo(request):
    if request.method == 'POST':
        try:
            id_correo = request.POST.get('correos_data')
            desde = request.POST.get('fecha_desde')
            hasta = request.POST.get('fecha_hasta')
            disco = request.POST.get('numero_disco')
            tipo = request.POST.get('tipo_nuevo')
            fecha_ejecucion = request.POST.get('fecha_ejecucion')
            observaciones = request.POST.get('observaciones')
            solicitante = request.POST.get('solicitante')
            nuevo = BackupsCorreos()
            nuevo.desde = desde
            nuevo.hasta = hasta
            marca_disco  = DiscoBackups.objects.get(id_disco = disco)
            nuevo.disco_duro = marca_disco
            nuevo.motivo = tipo
            nuevo.fecha =  timezone.now()
            nuevo.observaciones = observaciones
            nuevo.solicitante =solicitante
            nuevo.usuario = request.user
            marca_correo = usuarioCorreos.objects.get(id_u_correo = id_correo)
            nuevo.correo = marca_correo 
            nuevo.fecha_ejecucion = fecha_ejecucion
            nuevo.save() 
            fecha_ejecucion = datetime.strptime(fecha_ejecucion, "%Y-%m-%d")
            evento = Calendario()
            evento.title = f"Backup para de correo {marca_correo.correo_usuario}"
            evento.descripcion = f"Backup del correo: {marca_correo.correo_usuario} por motivo de '{tipo}' a cargo de: {solicitante}"
            evento.start = (fecha_ejecucion + timedelta(hours=12)).isoformat()
            evento.end = (fecha_ejecucion + timedelta(hours=15)).isoformat()
            evento.color = '#ff8000'
            evento.estado = True
            evento.activo = True
            evento.save()

            return redirect(f"{reverse('backups_correos')}?success=true")
        except Exception as e:
            return redirect(f"{reverse('backups_correos')}?error=true")
    
    return redirect('backups_correos')
 

def eliminar_correo_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = BackupsCorreos.objects.get(id_backup_correos=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse('backups_correos')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('backups_correos')}?error=true")
    
    return redirect('backups_correos')

def activar_correo_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = BackupsCorreos.objects.get(id_backup_correos=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse('backups_correos')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('backups_correos')}?error=true")
    return redirect('backups_correos')

def agregar_archivo_backup(request):
    if request.method == 'POST':  
        id = request.POST.get('id_backup')
        actualizar = BackupsCorreos.objects.get(id_backup_correos=id)
        try:
            if request.POST.get('enlace_archivo'):
                enlace = request.POST.get('enlace_archivo')
                actualizar.ubicacion = enlace
            else:
                doc = request.FILES.get('archivo')
                def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
                    query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
                    if carpeta_padre_id:
                        query += f" and '{carpeta_padre_id}' in parents"
                    resultados = service.files().list(q=query, fields="files(id, name)").execute()
                    folders = resultados.get('files', [])
                    if folders:
                        return folders[0]['id']
                    else:
                        file_metadata = {
                            'name': carpeta_nombre,
                            'mimeType': 'application/vnd.google-apps.folder',
                        }
                        if carpeta_padre_id:
                            file_metadata['parents'] = [carpeta_padre_id]

                        carpeta = service.files().create(body=file_metadata, fields='id').execute()
                        print(f"[DEBUG] Carpeta '{carpeta_nombre}' creada con ID: {carpeta['id']}")
                        return carpeta['id']
                    
                service = authenticate_google_drive()
                carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA VILASECA MODULO BACKUPS')
                carpeta_empleado_id = obtener_o_crear_carpeta('BACKUPS CORREOS', carpeta_padre_id=carpeta_documentos_id)
                nombre = actualizar.correo.correo_usuario
                fecha_actual = timezone.now()
                archivo_guardado_nombre = f"{nombre}_{fecha_actual.strftime('%Y%m%d_%H%M%S')}"
                temp_file_path = os.path.join(settings.MEDIA_ROOT, archivo_guardado_nombre)
                with open(temp_file_path, 'wb') as f:
                    for chunk in doc.chunks(): 
                        f.write(chunk)
                file_metadata = {
                    'name': archivo_guardado_nombre,
                    'parents': [carpeta_empleado_id]
                }
                media = MediaFileUpload(temp_file_path, mimetype=doc.content_type)
                file_drive = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"[DEBUG] Archivo subido a Google Drive con ID: {file_drive['id']}")
                ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"
                def eliminar_archivo():
                    try:
                        os.remove(temp_file_path)
                        print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                    except Exception as e:
                        print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")
                Timer(300, eliminar_archivo).start()
                actualizar.ubicacion = ruta_final
       
            actualizar.save()
            return redirect(f"{reverse('backups_correos')}?subir=true")
        except Exception as e:
            return redirect(f"{reverse('backups_correos')}?error=true")
    
    return redirect('backups_correos')
    


def evaluar_backups_correos(request):
    datos = BackupsCorreos.objects.filter(activo= True)
    correos = usuarioCorreos.objects.exclude(asunto=None)
    discos = DiscoBackups.objects.all()
    usuarios = User.objects.filter(is_active = True)
    return render(request, 'backups/backup_correo.html', {'datos':datos, 'correos':correos, 'discos': discos, 'usuarios':usuarios})


def editar_backups_correos(request):
    if request.method == 'POST':
        try:
            id_editar = request.POST.get('id_editar')
            id_correo = request.POST.get('correos_data_editar')
            desde = request.POST.get('fecha_desde_editar')
            hasta = request.POST.get('fecha_hasta_editar')
            disco = request.POST.get('numero_disco_editar')
            tipo = request.POST.get('tipo_nuevo_editar')
            observaciones = request.POST.get('observaciones_editar')
            solicitante = request.POST.get('solicitante_editar')

            editar = BackupsCorreos.objects.get(id_backup_correos = id_editar)
            editar.desde = desde
            editar.hasta = hasta
            marca_disco  = DiscoBackups.objects.get(id_disco = disco)
            editar.disco_duro = marca_disco
            editar.motivo = tipo
            editar.fecha =  timezone.now()
            editar.observaciones = observaciones
            editar.solicitante = solicitante
            editar.usuario = request.user
            marca_correo = usuarioCorreos.objects.get(id_u_correo = id_correo)
            editar.correo = marca_correo
            editar.save() 
            
            return redirect(f"{reverse('backups_correos')}?editar=true")
        except Exception as e:
            print(e)
            return redirect(f"{reverse('backups_correos')}?error=true")

    
    return redirect('backups_correos')


def editar_backups_nuevo(request):
    if request.method == 'POST':
        try:
            id_editar = request.POST.get('id_editar')
            gestion = request.POST.get('gestion_editar')
            fecha = request.POST.get('fecha_ejecucion_editar')
            id = request.POST.get('equipo_verificar_editar')
            periodo = request.POST.get('periodo_editar')
            id_emplea = request.POST.get('empleado_verificar_editar')
            obs = request.POST.get('observaciones_editar')
            tipo_nuevo = request.POST.get('tipo_nuevo_editar')

            marcas = User.objects.get(id=id_emplea)
            nuevo = Backups.objects.get(id_backup = id_editar)
       
            nuevo.fecha = fecha
            nuevo.gestion = gestion
            marca = Equipos.objects.get(id_equipo=id)
            user = User.objects.get(id = id_emplea)
            nuevo.usuario = user
            nuevo.equipo = marca
            nuevo.usuario = marcas
            nuevo.periodo = periodo
            nuevo.observaciones = obs
            nuevo.tipo_backup = tipo_nuevo
            nuevo.save()

            return redirect(f"{reverse('registro_backups')}?editar=true")

        except Exception as e:
            return redirect(f"{reverse('registro_backups')}?error=true")
    
    return redirect('registro_backups')


def eliminar_equipo_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = Backups.objects.get(id_backup=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse('registro_backups')}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse('registro_backups')}?error=true")
    
    return redirect('registro_backups')

def activar_equipo_backup(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = Backups.objects.get(id_backup=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse('registro_backups')}?activar=true")

        except Exception as e:
            return redirect(f"{reverse('registro_backups')}?error=true")
    return redirect('registro_backups')





def calendario(request):
    eventos = Calendario.objects.all()
    return render(request, 'calendario.html', {'eventos': eventos})

def calendario_emple(request):
    eventos = Calendario.objects.all()
    return render(request, 'calendario_emple.html', {'eventos': eventos})

def obtener_eventos(request):
    eventos = Calendario.objects.all()
    eventos_data = [{
        'id': evento.id,
        'title': evento.title,
        'descripcion2': evento.descripcion,
        'start': evento.start.isoformat(),
        'end': evento.end.isoformat(),
        
        'color': evento.color,
    } for evento in eventos]

     
    return JsonResponse(eventos_data, safe=False)


@csrf_exempt  
def crear_evento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data) 
            title = data.get('title')
            descripcion = data.get('descripcion')  
            start = data.get('start')
            end = data.get('end')
            color = data.get('color')
            if not all([title, descripcion, start, end,color]):
                return JsonResponse({'error': 'Faltan datos requeridos'}, status=400)
            nuevo_evento = Calendario.objects.create(
                title=title,
                descripcion=descripcion,
                start=start,
                end=end,
                color = color
            )

            return JsonResponse({'message': 'Evento creado exitosamente', 'id': nuevo_evento.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

 

@csrf_exempt
def eliminar_evento(request, event_id):
    if request.method == 'POST':
        try:
            evento = Calendario.objects.get(id=event_id)
            evento.delete()
            return JsonResponse({'status': 'success', 'message': 'Evento eliminado correctamente'})
        
        except Calendario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evento no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



@csrf_exempt
def editar_evento(request, event_id):
    if request.method == 'POST':
        try:
            evento = Calendario.objects.get(id=event_id)
            data = json.loads(request.body)
            evento.title = data.get('title', evento.title)
            evento.descripcion = data.get('descripcion', evento.descripcion)
            evento.start = data.get('start')
            evento.end = data.get('end')
            evento.color = data.get('color', evento.color)
            evento.save()

            return JsonResponse({'status': 'success', 'message': 'Evento actualizado correctamente'})
        
        except Calendario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evento no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def agregar_mantenimiento(request):
    if request.method == 'POST':
        try:
            equipo_seleccionado = request.POST.get('equipo_seleccionado')
            tipos = request.POST.get('tipos_mantenimientos')
            fecha_registro = request.POST.get('fecha_registro')
            fecha_solucion = request.POST.get('fecha_solucion')
            cambiar_empleado = request.POST.get('cambiar_empleado')
            diagnostico = request.POST.get('diagnostico')
            solucion = request.POST.get('solucion')
            nuevo = Mantenimientos()
            nuevo.tipo = tipos
            nuevo.fecha_culminada = fecha_solucion
            marca = Equipos.objects.get(id_equipo = equipo_seleccionado)
            nuevo.equipo = marca
            dato_empleado = User.objects.get(id = cambiar_empleado)
            nombre = dato_empleado.first_name + dato_empleado.last_name
            nuevo.encargado = dato_empleado
            nuevo.diagnostico = diagnostico
            nuevo.solucion = solucion
            if tipos == 'PREVENTIVO':
                nuevo.fecha_planificada = fecha_registro
                fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d")
                fecha_solucion = datetime.strptime(fecha_solucion, "%Y-%m-%d")
                evento = Calendario()
                evento.title = f"Mantenimiento del Equipo {marca.codigo_equipo}"
                evento.descripcion = f"Mantenimiento PREVENTIVO del Equipo: {marca.codigo_equipo} - {marca.nombre} a cargo de: {nombre}"
                evento.start = fecha_registro.isoformat() 
                evento.end = fecha_solucion.isoformat()  
                evento.color = '#88dc65'
                evento.save()
            else:
                nuevo.fecha_realizada = fecha_registro
        
            
            nuevo.save()
            
            return redirect(f"{reverse('mantenimiento')}?success=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse('mantenimiento')}?error=true")

    return redirect('mantenimiento')


def backups_sistemas(request):
    datos = BackupSistemas.objects.all() 
    usuarios = User.objects.all()
    sistemas = Softwares.objects.all()
    discos = DiscoBackups.objects.all()
    areas = Areas.objects.all()
    oficinas = Oficina.objects.all()
      
    return render(request, 'backups/backup_sistema.html', {'datos': datos, 'usuarios': usuarios, 'sistemas': sistemas, 'discos': discos , 'areas': areas, 'oficinas': oficinas})



def eliminar_empleo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = Empleo.objects.get(id_empleo=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse(datos_contratos)}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse(datos_contratos)}?error=true")
    
    return redirect(datos_contratos)   

def activar_empleo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = Empleo.objects.get(id_empleo=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse(datos_contratos)}?activar=true")
        except Exception as e:
            return redirect(f"{reverse(datos_contratos)}?error=true")
    return redirect(datos_contratos)   



def eliminar_cuentas_email(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = usuarioCorreos.objects.get(id_u_correo=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse(generar_contrasenas)}?desactivar=true")

        except Exception as e:
            return redirect(f"{reverse(generar_contrasenas)}?error=true")
    
    return redirect(generar_contrasenas)   

def activar_cuentas_email(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = usuarioCorreos.objects.get(id_u_correo=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse(generar_contrasenas)}?activar=true")

        except Exception as e:
            return redirect(f"{reverse(generar_contrasenas)}?error=true")
    
    return redirect(generar_contrasenas)   


def cargar_ciudades(request, id_departamento):
    ciudades = Ciudad.objects.filter(departamento_id=id_departamento).all()
    ciudad_data = [{"id_ciudad": ciudad.id_ciudad, "ciudad": ciudad.ciudad} for ciudad in ciudades]
    return JsonResponse({"ciudades": ciudad_data})


def listar_oficinas(request):
    datos = Oficina.objects.all()
    departamentos = Departamento.objects.all()
    return render(request, 'oficina/oficina.html', {'datos': datos, 'departamentos': departamentos })


def listar_cargos(request):
    datos = AreasCargos.objects.all()
    areas = Areas.objects.filter(activo = True)
    return render(request, 'oficina/cargos.html', {'datos': datos, 'areas':areas})


def agregar_empresa_datos(request):
    if request.method == 'POST':
        try:
            area = request.POST.get('area')
            planillado = request.POST.get('planillado')
            personal_cargo = request.POST.get('personal_cargo')
            cargo = request.POST.get('cargo')

            crear = AreasCargos()
            crear.cargo =  cargo
            crear.fecha_registro = timezone.now()
            crear.planillado = planillado
            marca = Areas.objects.get(id_area = area)
            crear.area = marca
            crear.subpersonal = personal_cargo
            crear.save()

            return redirect(f"{reverse(listar_cargos)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(listar_cargos)}?error=true")
    
    return redirect(listar_cargos)   

def agregar_oficina(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            departamento = request.POST.get('departamento')
            direccion = request.POST.get('direccion')
            latitud = request.POST.get('latitud')
            longitud = request.POST.get('longitud')

            crear = Oficina()
            crear.nombre =  nombre
            
            marca = Departamento.objects.get(id_depa = departamento)
            crear.departamento = marca
            crear.direccion = direccion
            crear.latitud = latitud
            crear.longitud = longitud
            crear.fecha = timezone.now()
            crear.save()
             

            return redirect(f"{reverse(listar_oficinas)}?success=true")

        except Exception as e:
            return redirect(f"{reverse(listar_oficinas)}?error=true")
    
    return redirect(listar_oficinas) 



    
def eliminar_datos_oficina(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            
            actualizar = Oficina.objects.get(id_oficina=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse(listar_oficinas)}?desactivar=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse(listar_oficinas)}?error=true")
    
    return redirect(listar_oficinas)   

def activar_datos_oficina(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
          
            actualizar = Oficina.objects.get(id_oficina=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse(listar_oficinas)}?activar=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse(listar_oficinas)}?error=true")
    
    return redirect(listar_oficinas)   


    
def eliminar_cargo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_eliminar')
            actualizar = AreasCargos.objects.get(id_area=id)
            actualizar.activo = False
            actualizar.save()
            return redirect(f"{reverse(listar_cargos)}?desactivar=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse(listar_cargos)}?error=true")
    
    return redirect(listar_cargos)   


def activar_cargo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id_activar')
            actualizar = AreasCargos.objects.get(id_area=id)
            actualizar.activo = True
            actualizar.save()
            return redirect(f"{reverse(listar_cargos)}?activar=true")

        except Exception as e:
            print(e)
            return redirect(f"{reverse(listar_cargos)}?error=true")
    
    return redirect(listar_cargos)   


def editar_datos_oficina(request):
    if request.method == 'POST':
        try:
            nombre_editar = request.POST.get('nombre_editar')
            departamento_editar = request.POST.get('departamento_editar')
            direccion_editar = request.POST.get('direccion_editar')
            latitud_editar = request.POST.get('latitud_editar')
            longitud_editar = request.POST.get('longitud_editar')
            id_oficina_editar =  request.POST.get('id_oficina_editar')
            editar = Oficina.objects.get(id_oficina=id_oficina_editar)
            editar.nombre = nombre_editar
            marca = Departamento.objects.get(id_depa=departamento_editar)
            editar.departamento = marca
            editar.direccion = direccion_editar
            editar.nombre = nombre_editar
        
            latitud_correcta = latitud_editar.replace(',', '.')  
            editar.latitud = float(latitud_correcta)
            longitud_correcta = longitud_editar.replace(',', '.')  
            editar.longitud = float(longitud_correcta)
            editar.save()
            return redirect(f"{reverse(listar_oficinas)}?editar=true")

        except Exception as e:
 
            return redirect(f"{reverse(listar_oficinas)}?error=true")

    
    return redirect(listar_oficinas) 


def agregar_backup_sistema(request):
    if request.method == 'POST':
        try:
            sistema_data = request.POST.get('sistema_data')
            periodo = request.POST.get('periodo')
            solicitante = request.POST.get('solicitante')
            observaciones = request.POST.get('observaciones')
            tipo_backup = request.POST.get('tipo_backup')
            geston = request.POST.get('gestion')
            oficina = request.POST.get("oficina")
            numero_disco = request.POST.get('numero_disco')
            fecha_ejecucion = request.POST.get('fecha_ejecucion')
            crear = BackupSistemas()
            marca_id = Softwares.objects.get(id_sistema = sistema_data)
            areas = request.POST.get('area')
            crear.sistema = marca_id
            crear.periodo = periodo
            crear.tipo = tipo_backup
            crear.observaciones = observaciones
            crear.gestion = geston
            masrca_area = Areas.objects.get(id_area = areas)
            crear.area = masrca_area
            crear.fecha_planificada = fecha_ejecucion
            marca_disco = DiscoBackups.objects.get(id_disco = numero_disco)
            crear.disco_duro = marca_disco
            marca_ofi = Oficina.objects.get(id_oficina = oficina)
            crear.oficina = marca_ofi
            crear.save()

            return redirect(f"{reverse(backups_sistemas)}?success=true")

        except Exception as e:
  
            return redirect(f"{reverse(backups_sistemas)}?error=true")
    
    return redirect(backups_sistemas)   



def subir_archivo_sistema(request):
    if request.method == 'POST':
        
        id = request.POST.get('id_backup')
        actualizar = BackupsCorreos.objects.get(id_backup_correos=id)

        try:
            if request.POST.get('enlace_archivo'):
                enlace = request.POST.get('enlace_archivo')
                actualizar.ubicacion = enlace
            else:
                doc = request.FILES.get('archivo')

                def obtener_o_crear_carpeta(carpeta_nombre, carpeta_padre_id=None):
                    query = f"mimeType='application/vnd.google-apps.folder' and name='{carpeta_nombre}'"
                    if carpeta_padre_id:
                        query += f" and '{carpeta_padre_id}' in parents"
                    resultados = service.files().list(q=query, fields="files(id, name)").execute()
                    folders = resultados.get('files', [])

                    if folders:
                        return folders[0]['id']
                    else:
                        file_metadata = {
                            'name': carpeta_nombre,
                            'mimeType': 'application/vnd.google-apps.folder',
                        }
                        if carpeta_padre_id:
                            file_metadata['parents'] = [carpeta_padre_id]

                        carpeta = service.files().create(body=file_metadata, fields='id').execute()
                        print(f"[DEBUG] Carpeta '{carpeta_nombre}' creada con ID: {carpeta['id']}")
                        return carpeta['id']
                    
                service = authenticate_google_drive()
                carpeta_documentos_id = obtener_o_crear_carpeta('SISTEMA VILASECA MODULO BACKUPS')
                carpeta_empleado_id = obtener_o_crear_carpeta('BACKUPS CORREOS', carpeta_padre_id=carpeta_documentos_id)
                nombre = actualizar.correo.correo_usuario
                fecha_actual = timezone.now()
                archivo_guardado_nombre = f"{nombre}_{fecha_actual.strftime('%Y%m%d_%H%M%S')}"
                temp_file_path = os.path.join(settings.MEDIA_ROOT, archivo_guardado_nombre)
                with open(temp_file_path, 'wb') as f:
                    for chunk in doc.chunks(): 
                        f.write(chunk)
                file_metadata = {
                    'name': archivo_guardado_nombre,
                    'parents': [carpeta_empleado_id]
                }
                media = MediaFileUpload(temp_file_path, mimetype=doc.content_type)
                file_drive = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"[DEBUG] Archivo subido a Google Drive con ID: {file_drive['id']}")
                ruta_final = f"https://drive.google.com/file/d/{file_drive['id']}/view"
                def eliminar_archivo():
                    try:
                        os.remove(temp_file_path)
                        print(f"[DEBUG] Archivo temporal {temp_file_path} eliminado.")
                    except Exception as e:
                        print(f"[ERROR] No se pudo eliminar el archivo temporal {temp_file_path}. Error: {str(e)}")
                Timer(300, eliminar_archivo).start()
                actualizar.ubicacion = ruta_final
       
            actualizar.save()
            return redirect(f"{reverse('backups_correos')}?subir=true")
        except Exception as e:
            return redirect(f"{reverse('backups_correos')}?error=true")
    
    return redirect('backups_correos')
    
 
def verificar_b_sistema(request):
    if request.method == 'POST':
        try:
            id_d_verificar = request.POST.get('id_d_verificar')
            empleado = request.POST.get('empleado_verificar')  
            marca = User.objects.get(id = empleado)       
            disco = request.POST.get('numero_disco_verificar')
            mdisco = DiscoBackups.objects.get(id_disco = disco)
            observaciones_verificar = request.POST.get('observaciones_verificar')
            verificar = BackupSistemas.objects.get(id_b_verificar = id_d_verificar)
            verificar.asignado = marca
            verificar.disco_verificado = mdisco.numero
            verificar.fecha_verificada = timezone.now()
            verificar.observaciones = observaciones_verificar
            verificar.save()
            return redirect(f"{reverse(backups_sistemas)}?verificar=true")

        except Exception as e:
            return redirect(f"{reverse(backups_sistemas)}?error=true")
    
    return redirect(backups_sistemas) 
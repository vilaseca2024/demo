from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import User, Group



class Departamento(models.Model):
    id_depa = models.AutoField(primary_key=True)
    departamento = models.CharField(max_length=25)
    expedido = models.CharField(max_length=5, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'departamento'

class Areas(models.Model):
    id_area = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(null=True)
    area = models.CharField(max_length=50, null=True)
    activo = models.BooleanField(default=True)
 
    class Meta:
        db_table = 'areas'

class AreasCargos(models.Model):
    id_area = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(null=True)
    cargo = models.CharField(max_length=50, null=True)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True, blank=True)
    planillado = models.CharField(max_length=50, null=True)
    subpersonal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
 
    class Meta:
        db_table = 'areas_cargos'
        
class Oficina(models.Model):
    id_oficina = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    nombre = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=200, null=True)
    latitud = models.FloatField(null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True) 
    longitud = models.FloatField(null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'oficinas'

class BajaCorreosUsuarios(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    correo = models.CharField(max_length=50, null=True)
    correo_alt = models.CharField(max_length=50, null=True) 
    fecha = models.DateField(null=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    observacion = models.CharField(max_length=150,null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'baja_correo_usuario'


   
class AsignacionCorreosUsuarios(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    correo = models.CharField(max_length=50, null=True)
    correo_alt = models.CharField(max_length=50, null=True)
    fecha = models.DateField(null=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    observacion = models.CharField(max_length=150,null=True)
    baja = models.ForeignKey(BajaCorreosUsuarios, on_delete=models.CASCADE,null = True, blank=True)
    activo = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)
    class Meta:
        db_table = 'asignar_correo_usuario'


class TipoContrasenaEquipos(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'tipo_equipo_contrasena'


class MotivoCambio(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'motivo_cambio_contrasena'

class EstadoCivil(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'estado_civil'

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=15)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'genero'

class Sangre(models.Model):
    id_sangre = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'sangre'

class ClasificacionGrupo(models.Model):
    id_clas = models.AutoField(primary_key=True)
    clasificacion = models.CharField(max_length=15)
    rango_inicio = models.IntegerField(null=False)
    rango_fin = models.IntegerField(null=False)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'clasificacion_grupo'

class Generacion(models.Model):
    id_generacion = models.AutoField(primary_key=True)
    generacion = models.CharField(max_length=15)
    rango_inicio = models.IntegerField(null=False)
    rango_fin = models.IntegerField(null=False)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'generacion'

class DatosPersonal(models.Model):
    id_datos = models.AutoField(primary_key=True)
    empleado_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ci = models.IntegerField(null=True)
    complemento = models.CharField(max_length=5, null=True)
    expedido = models.CharField(max_length=5,null=True)
    nombre = models.CharField(max_length=30, null=True)
    ap_paterno = models.CharField(max_length=30,null=True)
    ap_materno = models.CharField(max_length=30, null=True)
    fecha_nacimiento = models.DateField(null=True)
    completo = models.BooleanField(default=False)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    tipo_sangre = models.CharField(max_length=10, null=True)
    alergias= models.CharField(max_length=200,null=True)
    
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'datos_personal'
        
class FilePersonal(models.Model):
    id_file = models.AutoField(primary_key=True)
    empleado_id = models.ForeignKey(DatosPersonal, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'file_personal'

class Certificados(models.Model):
    id_certificado = models.AutoField(primary_key=True)
    fecha_solicitud = models.DateField( null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    fecha_modificado = models.DateTimeField(auto_now_add=True, null=True)
    correo = models.CharField(max_length=100,null=False)
    dirigido = models.CharField(max_length=50,null=False)
    id_dirigido = models.IntegerField(null=True)
    emitido = models.CharField(max_length=50,null=True)
    tipo = models.CharField(max_length=20,null=True)
    estado = models.IntegerField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activo = models.BooleanField(default=True)
    gestion = models.IntegerField(null=True)
    requerimiento = models.CharField(max_length=250,null=True)
    drive  = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'solicitudes'

class CertificadoAprobados(models.Model):
    id_certificado_a = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Certificados, on_delete=models.CASCADE, null=True)
    codigo = models.CharField(max_length=100,null=False)
    referencia = models.CharField(max_length=100,null=False)
    dirigido = models.CharField(max_length=50,null=False)
    id_dirigido = models.IntegerField(null=True)
    correo = models.CharField(max_length=100,null=True)
    emitido = models.CharField(max_length=50,null=True)
    fecha_emision = models.DateTimeField(auto_now_add=True, null=True)
    adjunto = models.FileField(upload_to='certificados/', null=True, blank=True) 
    tipo = models.CharField(max_length=20,null=True)
    estado = models.IntegerField(null=True)
    usuario_modificado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gestion = models.IntegerField(null=True)
    correlativo = models.IntegerField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal,on_delete=models.CASCADE, null=True)
    cierre = models.BooleanField(default=True)
    drive = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'certificados'

class EstadoCertificado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(Certificados, on_delete=models.CASCADE, null=True)
    gestion = models.IntegerField(null=True)
    correlativo = models.IntegerField(null=True)
    estado = models.CharField(max_length=50,null=False)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    observacion = models.CharField(max_length=200,null=False)
    usuario_modificado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'estado_certificado'




class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
    ciudad = models.CharField(max_length=30, null=False)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'ciudad'

    


class TipoContrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    contrato = models.CharField(max_length=35)
    descripcion = models.CharField(max_length=35)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'tipo_contrato' 

class TipoRegistro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    registro = models.CharField(max_length=35)
    descripcion = models.CharField(max_length=35)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'tipo_registro' 

class ClasificacionAnti(models.Model):
    id_antiguedad = models.AutoField(primary_key=True)
    antiguedad = models.IntegerField(null=False)
    rango_inicio = models.IntegerField(null=True)
    rango_fin = models.IntegerField(null=True)
    descripcion = models.CharField(max_length=35)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'clasificacion_anti' 


class ContactosPersonal(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    empleado_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    celular = models.IntegerField(null=True)
    mapa = models.BooleanField(default=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True)
    direccion =models.CharField(max_length=200, null=True)
    latitud = models.FloatField(null=True)
    longitud = models.FloatField(null=True)
    contacto1_nombre = models.CharField(max_length=50, null=True)
    contacto1_parentesco = models.CharField(max_length=50, null=True)
    contacto1_numero = models.IntegerField(null=True)
    contacto2_nombre = models.CharField(max_length=50, null=True)
    contacto2_parentesco = models.CharField(max_length=50, null=True)
    contacto2_numero = models.IntegerField(null=True)
    hijos = models.BooleanField(null=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    activo = models.BooleanField(default=True)
    foto_puerta = models.ImageField(upload_to='puertas/', null=True, blank=True)
    class Meta:
        db_table = 'contacto_personal'

class Empleo(models.Model):
    id_empleo = models.AutoField(primary_key=True)
    empleado_id = models.ForeignKey(DatosPersonal, on_delete=models.CASCADE, null=True)
    
    codigo_trabajador= models.CharField(max_length=20, null=False)
    fecha_registro = models.DateTimeField(null=False)
    tipo_registro = models.ForeignKey(TipoRegistro, on_delete=models.CASCADE, null=True)
    nombre_trab = models.CharField(max_length=100, null=True)
    numero_trabajo = models.IntegerField(null=True)
    whatsapp = models.IntegerField(null=True)
    nro_interno= models.IntegerField(null=True)
    correo_corp = models.ForeignKey(AsignacionCorreosUsuarios, on_delete=models.CASCADE, null=True)
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE, null=True)
    antiguo = models.BooleanField(null=True)
    inicio_contrato = models.DateField(null=False)
    clasificacion = models.ForeignKey(ClasificacionAnti, on_delete=models.CASCADE, null=True)
    modalidad = models.CharField(max_length=20)
    fecha_modificacion = models.DateTimeField(auto_now_add=True, null=True)
    
    activo = models.BooleanField(default=True)
    centro_trabajo = models.ForeignKey(Oficina, on_delete=models.CASCADE, null=True)
    clasificacion = models.ForeignKey(AreasCargos, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'empleo'






class ClasificacionFile(models.Model):
    id_code_file = models.AutoField(primary_key=True)
    modalidad = models.CharField(max_length=30)
    siglas = models.CharField(max_length=10, unique=True)   
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'clasificacion_file'

class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'foto'


class HojaVida(models.Model):
    id_hoja = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'hoja_vida'

class Croquis(models.Model):
    id_croquis = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    drive  = models.CharField(max_length=200, null=True) 
    class Meta:
        db_table = 'croquis'

class Memorandum(models.Model):
    id_memorandum = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True)
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'memorandum'


class CartaPresentacion(models.Model):
    id_carta_presentacion = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    drive  = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'carta_presentacion'




class Varios(models.Model):
    id_varios = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    drive  = models.CharField(max_length=200, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'varios'

class Carnet(models.Model):
    id_carnet = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    drive  = models.CharField(max_length=200, null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'carnet'

class LuzAgua(models.Model):
    id_factura_luz = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True)
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'factura_luz'


class Induccion(models.Model):
    id_induccion = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True)
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'induccion'

class Curriculum(models.Model):
    id_curriculum = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    drive  = models.CharField(max_length=200, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'curriculum'

class Felcc(models.Model):
    id_felcc = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField(  null=True, blank=True) 
    drive  = models.CharField(max_length=200, null=True)
    fecha_registro = models.DateField(null=False)
    fecha_emision = models.DateField(null=True)
    fecha_vencimiento = models.DateField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'felcc'

class Felcn(models.Model):
    id_felcn = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    drive  = models.CharField(max_length=200, null=True)
    fecha_emision = models.DateField(null=True)
    fecha_vencimiento = models.DateField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'felcn'


class Rejab(models.Model):
    id_rejab = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    fecha_emision = models.DateField(null=True)
    drive  = models.CharField(max_length=200, null=True)
    fecha_vencimiento = models.DateField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'rejab'


class CertificadoExterno(models.Model):
    id_certificado_externo = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    drive  = models.CharField(max_length=200, null=True)
    entidad = models.CharField(max_length=20, null=True)
    activo = models.BooleanField(default=True)
    tiempo = models.IntegerField(null=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'certificado_externo'


class CertificadoAcademico(models.Model):
    id_certificado_academico = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    fecha_egreso = models.DateField(null=True)
    drive  = models.CharField(max_length=200, null=True)
    titulo = models.CharField(max_length=20,null=True)
    tiempo = models.IntegerField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'certificado_academico'

class ConveniosContratos(models.Model):
    id_convenios_contratos = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    fecha_emision = models.DateField(null=True)
    drive  = models.CharField(max_length=200, null=True)
    entidad = models.CharField(max_length=20,null=True)
    tiempo = models.IntegerField(null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'convenios_contratos'

class PautasActuacion(models.Model):
    id_pautas = models.AutoField(primary_key=True)
    clasificacion = models.ForeignKey(ClasificacionFile, on_delete=models.CASCADE, null=True)
    ruta  = models.FileField( null=True, blank=True) 
    fecha_registro = models.DateField(null=False)
    drive  = models.CharField(max_length=200, null=True)
    activo = models.BooleanField(default=True)
    file = models.ForeignKey(FilePersonal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'pautas'

class ContratoEmpleado(models.Model):
    id_datos_contrato = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_registro = models.DateField(null=False)
    celular_trabajo = models.IntegerField(null=True)
    whatsapp_trabajo = models.IntegerField(null=True)
    numero_interno = models.IntegerField(null=True)
    correo_corporativo = models.CharField(max_length=100,null=True)
    estado_trabajador = models.CharField(max_length=20,null=True)
    tipo_contrato = models.ForeignKey(TipoContrato,on_delete=models.CASCADE, null=True)
    antiguedad = models.BooleanField(default=False)
    inicio_contrato = models.DateField(null=True)
    clasificacion_anti = models.ForeignKey(ClasificacionAnti, on_delete=models.CASCADE, null=True)
    modalidad_trabajo = models.CharField(max_length=10, null=False)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'contrato_empleado'

class Modulo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True) 
    class Meta:
        db_table = 'modulos'


class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    ver = models.BooleanField(default=False)
    agregar = models.BooleanField(default=False)
    editar = models.BooleanField(default=False)
    eliminar = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'permisos'
        
class DevolucionEquipo(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    lapzo = models.CharField(max_length=50,null=True)
    observaciones = models.CharField(max_length=150,null=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    equipo = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'devolucion_equipos'

class Asignacion(models.Model):
    id_asignacion = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    equipo = models.CharField(max_length=50)
    detalle = models.CharField(max_length=50)
    fecha_asignado = models.DateField(null=True)
    fecha_devuelto = models.DateField(null=True)
    estado = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    devolucion = models.ForeignKey(DevolucionEquipo, on_delete=models.CASCADE,  null=True, blank=True)  
    class Meta:
        db_table = 'asignacion_equipos'

class Equipos(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=80)
    fecha_registro = models.DateField(null=True)
    fecha_compra = models.DateField(null=True)
    modelo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=30)
    tamano = models.CharField(max_length=20)
    modelo = models.CharField(max_length=50)
    auxiliares = models.CharField(max_length=150, null=True)
    antiguo = models.BooleanField(default=False)
    qr = models.ImageField(upload_to='qr_equipo/', null=True, blank=True)
    codigo_equipo = models.CharField(max_length=20, null=True)
    imagen_1 = models.ImageField(upload_to='equipos/', null=True, blank=True)
    imagen_2 = models.ImageField(upload_to='equipos/', null=True, blank=True)
    imagen_3 = models.ImageField(upload_to='equipos/', null=True, blank=True)
    imagen_4 = models.ImageField(upload_to='equipos/', null=True, blank=True)
    imagen_0 = models.ImageField(upload_to='equipos/', null=True, blank=True)
    asignacion = models.ForeignKey(Asignacion, on_delete=models.CASCADE, null=True, blank=True)  
    devolucion = models.ForeignKey(DevolucionEquipo, on_delete=models.CASCADE, null=True, blank=True) 
    activo = models.BooleanField(default=True)
    estado = models.BooleanField(default=False, null=True)  
    class Meta:
        db_table = 'equipos_oficina'

 
class AsignadoEquipoCuenta(models.Model):
    id_cuenta_equipo = models.AutoField(primary_key=True)
    codigo_equipo = models.CharField(max_length=20, null=True)
    fecha_cambio = models.DateField(null=True)
    clave = models.CharField(max_length=100, null=True)
    estado = models.IntegerField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    class Meta:
        db_table = 'asignar_cuenta_eq'


class EquiposCuentas(models.Model):
    id_cuenta_equipo = models.AutoField(primary_key=True)
    equipo_id = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True)  
    fecha = models.DateField(null=True)
    datos = models.CharField(max_length=100, null=True)
    tipo = models.ForeignKey(TipoContrasenaEquipos, on_delete=models.CASCADE, null=True, blank=True)  
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    asignado_id = models.ForeignKey(AsignadoEquipoCuenta, on_delete=models.CASCADE, null=True, blank=True)  
    usuario_cuenta = models.CharField(max_length=20, null=True)
    observaciones = models.CharField(max_length=100, null=True)
    motivo = models.ForeignKey(MotivoCambio, on_delete=models.CASCADE, null=True, blank=True)  
    
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'equipo_cuentas'


class CambiosEquipos(models.Model):
    id_cambios = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    equipo = models.IntegerField(null=True)
    fecha = models.DateTimeField(null=True)
    descripcion = models.CharField(max_length=150,null=True)

    class Meta:
        db_table = 'cambios_equipos'



class usuarioCorreos(models.Model):
    id_u_correo = models.AutoField(primary_key=True)
    fecha = models.DateField(null=True)
    correo_usuario = models.CharField(max_length=50, null=True)
    correo_alt = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=10,null=True)
    observacion = models.CharField(max_length=100,null=True)
    adjunto = models.FileField(upload_to='correos/', null=True, blank=True) 
    asunto = models.CharField(max_length=200, null=True)
    activo = models.BooleanField(default=True)
    compartido = models.BooleanField(default=False)
    estado = models.IntegerField(null=True)
    asignado = models.ForeignKey(AsignacionCorreosUsuarios, on_delete=models.CASCADE, null=True, blank=True)  
    class Meta:
        db_table = 'usuario_correos'







class controlUsuario(models.Model):
    id_control = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    detalle = models.CharField(max_length=100,null=True)
    registro = models.ForeignKey(usuarioCorreos, on_delete=models.CASCADE, null=True, blank=True)  
    marca = models.CharField(max_length=100,null=True)
    tipo = models.IntegerField(null=True)
    anterior = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = 'control_crud'

class VerificacionCodigo(models.Model):
    codigo = models.CharField(max_length=10)
    tiempo_expiracion = models.DateTimeField()

    def __str__(self):
        return self.codigo
 

class auditoriaEquipos(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    detalle = models.CharField(max_length=200,null=True)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True)  
    drive = models.CharField(max_length=200,null=True)
    
    class Meta:
        db_table = 'auditoria_equipos'


class SolicitudServicioTecnico(models.Model):
    id_ticket = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    mensaje = models.CharField(max_length=500,null=True)
    fecha_respuesta = models.DateTimeField(null=True)
    diagnostico = models.CharField(max_length=200,null=True)
    accion = models.CharField(max_length=200,null=True)
    correccion = models.CharField(max_length=200,null=True)
    recomendacion = models.CharField(max_length=200,null=True)
    estado_final = models.CharField(max_length=200,null=True)
    observacion = models.CharField(max_length=200,null=True)
    estado = models.BooleanField(default=False)
    foto = models.CharField(max_length=500,null=True)
    codigo = models.CharField(max_length=10,null=True)
    
    class Meta:
        db_table = 'soporte_tecnico'

class Softwares(models.Model):
    id_sistema = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    nombre = models.CharField(max_length=50,null=True)
    enlace = models.CharField(max_length=200,null=True)
    puerto = models.IntegerField(null=True)
    ip = models.CharField(max_length=25,null=True)
    descripcion = models.CharField(max_length=200,null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'sistemas_informaticos'

class BajaCuentasSoftwares(models.Model):
    id_asignado = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.CharField(max_length=50,null=True)
    observacion = models.CharField(max_length=250,null=True)
    usuario_baja = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    class Meta:
        db_table = 'baja_cuentas_software'

class AsignarCuentasSoftwares(models.Model):
    id_asignado = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.CharField(max_length=50,null=True)
    observacion = models.CharField(max_length=250,null=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    baja = models.ForeignKey(BajaCuentasSoftwares, on_delete=models.CASCADE, null=True, blank=True) 
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'asig_cuentas_software'

class CuentasSoftwares(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    sistema = models.ForeignKey(Softwares, on_delete=models.CASCADE, null=True, blank=True) 
    usuario = models.CharField(max_length=50,null=True)
    tipo_usuario = models.CharField(max_length=20,null=True)
    contra = models.CharField(max_length=200,null=True)
    asignado = models.ForeignKey(AsignarCuentasSoftwares, on_delete=models.CASCADE, null=True, blank=True)  
    estado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'cuentas_software'

class BajaCuentaTeletrabajo(models.Model):
    id_baja = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    observaciones = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'baja_cuenta_teletrabajo'
    
class AsignarCuentaTeletrabajo(models.Model):
    id_asignado = models.AutoField(primary_key=True)
    observaciones = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField(null=True)
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    ip_equipo = models.CharField(max_length=20,null=True)
    tipo_acceso = models.CharField(max_length=50,null=True)
    firmware = models.CharField(max_length=20,null=True)
    dst = models.CharField(max_length=20,null=True)
    baja = models.ForeignKey(BajaCuentaTeletrabajo, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        db_table = 'asignar_cuenta_teletrabajo'


    

class CuentasTeletrabajo(models.Model):
    id_teletrabajo = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    ip_equipo = models.CharField(max_length=20,null=True)
    tipo_acceso = models.CharField(max_length=50,null=True)
    firmware = models.CharField(max_length=20,null=True)
    dst = models.CharField(max_length=20,null=True)
    activo = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=200, null=True)
    asignado = models.ForeignKey(AsignarCuentaTeletrabajo, on_delete=models.CASCADE, null=True, blank=True) 
    estado = models.BooleanField(default=False)


    class Meta:
        db_table = 'cuenta_teletrabajo'


class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return self.titulo
    

class EstadoBackups(models.Model):
    id_estado_b = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    periodo = models.CharField(max_length=20, null=True)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    estado = models.IntegerField(null=True)
    activo = models.BooleanField(default=True)
    informe_drive = models.CharField(max_length=200, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
   
    class Meta:
        db_table = 'estado_backup'


class AreasOficina(models.Model):
    id_area = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    area = models.DateTimeField(null=True)
    descripcion = models.CharField(max_length=200, null=True)
    activo = models.BooleanField(default=True)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, null=True, blank=True) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
   
    class Meta:
        db_table = 'area_oficina'

class DiscoBackups(models.Model):
    id_disco = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True) 
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    numero = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'disco_backup'

class VerificacionBackups(models.Model):
    id_backup = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    gestion = models.IntegerField(null=True)
    disco_duro = models.ForeignKey(DiscoBackups, on_delete=models.CASCADE, null=True, blank=True) 
    regional = models.CharField(max_length=20, null=True)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    obs = models.CharField(max_length=200, null=True)
    revisor_cambio = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    activo = models.BooleanField(default=True)
    fechar_verificacion = models.DateTimeField(null=True)
    class Meta:
        db_table = 'verificar_backup'

class Backups(models.Model):
    id_backup = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    gestion = models.IntegerField(null=True)
    periodo = models.CharField(max_length=20, null=True)
    regional = models.CharField(max_length=20, null=True)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    estado = models.ForeignKey(EstadoBackups, on_delete=models.CASCADE, null=True, blank=True) 
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    observaciones = models.CharField(max_length=200, null=True)
    verificar = models.ForeignKey(VerificacionBackups, on_delete=models.CASCADE, null=True, blank=True) 
    tipo_backup = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'backup'


class EstadoBackupsCorreos(models.Model):
    id_estado_b = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    regional = models.CharField(max_length=20, null=True) 
    estado = models.CharField(max_length=20, null=True)  
    correo = models.ForeignKey(usuarioCorreos, on_delete=models.CASCADE, null=True, blank=True) 
    total = models.IntegerField(null=True)
    usado = models.IntegerField(null=True)
    restante = models.IntegerField(null=True)  
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    class Meta:
        db_table = 'estado_backup_correo'

class BackupsCorreos(models.Model):
    id_backup_correos = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(null=True)
    fecha_ejecucion = models.DateTimeField(null=True)
    regional = models.CharField(max_length=20, null=True)
    ubicacion = models.CharField(max_length=200, null=True)
    disco_duro = models.ForeignKey(DiscoBackups, on_delete=models.CASCADE, null=True, blank=True) 
    correo = models.ForeignKey(usuarioCorreos, on_delete=models.CASCADE, null=True, blank=True) 
    tipo_correo = models.CharField(max_length=50, null=True)
    desde = models.DateField(null=True)
    hasta = models.DateField(null=True)
    motivo = models.CharField(max_length=50, null=True)
    observaciones = models.CharField(max_length=250, null=True)
    solicitante = models.CharField(max_length=50, null=True)
    estado = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    observaciones = models.CharField(max_length=200, null=True)
    estado = models.ForeignKey(EstadoBackupsCorreos, on_delete=models.CASCADE, null=True, blank=True) 
    class Meta:
        db_table = 'backup_correo'


class Calendario(models.Model):
    title = models.CharField(max_length=200)   
    descripcion = models.TextField(blank=True, null=True)   
    start = models.DateTimeField()   
    end = models.DateTimeField()  
    tipo = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=7, default='#00aae4') 
    area = models.CharField(max_length=20, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.BooleanField(default=True, null=True)
    activo = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.title

class Mantenimientos(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    fecha_planificada = models.DateTimeField(null=True)
    fecha_realizada = models.DateTimeField(null=True)
    fecha_culminada = models.DateTimeField(null=True)
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True, blank=True) 
    tipo = models.CharField(max_length=100, null=True)
    evaluacion_inicial = models.CharField(max_length=250, null=True)
    observaciones = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=20, null=True)
    activo = models.BooleanField(default=True)
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    diagnostico = models.CharField(max_length=200, null=True)
    solucion = models.CharField(max_length=200, null=True)


    class Meta:
        db_table = 'mantenimiento'

class BackupSistemas(models.Model):
    id_b_sistema = models.AutoField(primary_key=True)
    fecha_planificada = models.DateTimeField(null=True)
    fecha_realizada = models.DateTimeField(null=True)
    fecha_verificada = models.DateTimeField(null=True)
    gestion = models.IntegerField(null=True)
    disco_duro = models.ForeignKey(DiscoBackups, on_delete=models.CASCADE, null=True, blank=True) 
    disco_verificado = models.CharField(max_length=20,null=True)
    observaciones = models.CharField(max_length=250, null=True)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, null=True, blank=True) 
    asignado = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    sistema = models.ForeignKey(Softwares, on_delete=models.CASCADE, null=True, blank=True) 
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True, blank=True) 
    tipo = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=20, null=True)
    activo = models.BooleanField(default=True)
    periodo = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = 'backup_sistema'


 

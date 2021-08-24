from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Olt (models.Model):
	MAC_OLT = models.CharField(max_length =5, unique=True, primary_key=True)
	Modelo = models.CharField(max_length=50)
	Detalle= models.CharField(max_length=50)
	Marca =models.CharField(max_length=50)
	Capacidad = models.IntegerField()

	def __str__(self):
		valor = f"{self.Detalle }"
		return valor

class TarjetaOLT(models.Model):
	Numero_Tarjeta = models.IntegerField(unique=True)
	Capacidad = models.IntegerField()
	Olt = models.ForeignKey(Olt, on_delete=models.CASCADE , related_name="olts")

	def check_Olt(self):
		olts = self.Olt.olts.exclude(pk=self.pk).count()
		if olts >= self.Olt.Capacidad:
			return False
		return True

	def clean(self):
		if not self.check_Olt():
			raise ValidationError('ESTA OLT NO TIENE CAPACIDAD PARA MAS TARJETAS')
		

	def __str__(self):
		valor = f"{self.Olt} {self.Numero_Tarjeta}"
		return valor


class Distrito(models.Model):
	Nombre = models.CharField(max_length=50)
	Descripcion = models.CharField(max_length=50)

	def __str__(self):
		valor = f"{self.Nombre}"
		return valor

class VLAN (models.Model):
	ID = models.CharField(max_length=10, unique=True , primary_key= True)
	Numero= models.IntegerField()
	Detalle= models.CharField(max_length=50)
	Gemport= models.CharField(max_length=4)
	ServicePort= models.CharField(max_length=4)
	LineProfile= models.CharField(max_length=4)
	UserVlan= models.CharField(max_length=3)

	def __str__(self):
		valor = f"{self.ID} {self.Detalle}"
		return valor

class IP_Address(models.Model):
	ip = models.GenericIPAddressField(unique=True)
	Vlan = models.ForeignKey(VLAN, on_delete=models.PROTECT, related_name="ips")

	def __str__(self):
		valor = f"{self.ip} {self.Vlan.ID} {self.Vlan.Detalle}"
		return valor

	class Meta:
		ordering = ("ip",)

class Red_Alimentacion (models.Model):
	ID_FO =models.CharField(max_length=10, unique=True)
	Detalle_recorrido = models.CharField(max_length=50)
	Capacidad = models.IntegerField()
	Marca= models.CharField(max_length=50)


	def __str__(self):
		valor = f"{self.ID_FO} {self.Detalle_recorrido}"
		return valor

class Hilos_Alimentacion (models.Model):
	Tubillo= models.CharField(max_length=20)
	Color_hilo = models.CharField(max_length=20)
	FO_Alimentacion= models.ForeignKey(Red_Alimentacion, on_delete=models.CASCADE, related_name="alimentacion")
	Distrito= models.ForeignKey(Distrito, on_delete=models.CASCADE, null=True)

	def check_alimentacion(self):
		alimentacion = self.FO_Alimentacion.alimentacion.exclude(pk=self.pk).count()
		if alimentacion >= self.FO_Alimentacion.Capacidad:
			return False
		return True

	def clean(self):
		if not self.check_alimentacion():
			raise ValidationError('ESTA FIBRA YA NO TIENE MAS HILOS DISPONIBLES')
	
	def estado(self):
		if self.puertos.all():
			return 'Ocupado'
		return 'Reserva'


	def __str__(self):
		valor = f"{self.pk} {self.Tubillo} {self.Color_hilo}"
		return valor

class Red_Distribucion (models.Model):
	ID_FO= models.CharField(max_length=20, unique=True)
	Detalle_recorrido= models.CharField(max_length=50)
	Capacidad= models.IntegerField()
	Marca= models.CharField(max_length=30)
	Distrito= models.ForeignKey(Distrito, on_delete=models.CASCADE)

	def __str__(self):
		valor = f"{self.Detalle_recorrido} {self.Distrito}"
		return valor

class Distribucion_Puertos_a_Distrito(models.Model):
	Numero_Puerto = models.IntegerField()
	Descripcion= models.CharField(max_length=30)
	Tarjeta= models.ForeignKey(TarjetaOLT, on_delete=models.CASCADE)
	VLAN =models.ForeignKey(VLAN, on_delete=models.CASCADE)
	ID_Fibra=models.ForeignKey(Hilos_Alimentacion, on_delete=models.CASCADE, unique=True, related_name="puertos")

	def __str__(self):
		valor = f"{self.Tarjeta} {self.Numero_Puerto}"
		return valor

class NAP (models.Model):
	Codigo = models.CharField(max_length=10, unique=True)
	Hilo= models.CharField(max_length=10)
	Tubillo= models.CharField(max_length=10)
	Capacidad= models.IntegerField()
	Ubicacion = models.CharField(max_length=60)
	FO_Distribucion = models.ForeignKey(Red_Distribucion, on_delete=models.CASCADE,related_name="distribucion" )
	Spliiter_principal= models.ForeignKey(Distribucion_Puertos_a_Distrito, on_delete= models.CASCADE, null=True, blank=True)

	def check_distribucion(self):
		distri = self.FO_Distribucion.distribucion.exclude(pk=self.pk).count()
		if distri >= self.FO_Distribucion.Capacidad:
			return False
		return True

	def clean(self):
		if not self.check_distribucion():
			raise ValidationError('ESTA DISTRIBUCION DE FIBRA NO ADMITE MAS NAP')


	def avilables(self):
		clients = self.clients.all().count()
		if not clients:
			clients = 0
		return int(self.Capacidad - clients)

	def __str__(self):
		valor = f"{self.Codigo}"
		return valor


class Plan_Contratado (models.Model):
	Velocidad= models.IntegerField()
	Detalle= models.CharField(max_length=50)
	tabla_trafico= models.CharField(max_length=50)

	def __str__(self):
		valor = f"{self.Velocidad} {self.Detalle}"
		return valor

class Cliente (models.Model):
	
	Nombre = models.CharField(max_length= 50)
	Direccion = models.CharField(max_length=60)
	Sn_auth= models.CharField(max_length= 50, unique=True)
	Plan_Contratado= models.ForeignKey(Plan_Contratado, on_delete=models.CASCADE)
	Numero_ont= models.IntegerField(unique=True)
	Numero_ServicePort= models.IntegerField(unique=True)
	Distrito= models.ForeignKey(Distrito, on_delete=models.CASCADE)
	Nap= models.ForeignKey(NAP, on_delete=models.CASCADE, related_name="clients")
	Actualizar_Script = models.BooleanField(default=True)
	Script = models.TextField(null=True, editable=False)
	IP= models.OneToOneField(IP_Address, on_delete=models.PROTECT, null=True, editable=False, related_name="cliente")

	def check_Nap(self):
		clients = self.Nap.clients.exclude(pk=self.pk).count()
		if clients >= self.Nap.Capacidad:
			return False
		return True
		
	def asignacion (self):
		vlan = self.Nap.Spliiter_principal.VLAN
		ip = vlan.ips.filter(cliente__isnull=True).first()
		return ip

	def clean(self):
		if not self.check_Nap():
			raise ValidationError('No existen puertos disponibles en esta NAP')
		if not self.asignacion():
			raise ValidationError('NO EXISTE UNA IP DISPONIBLE PARA ASIGNAR')	

	def save(self, *args, **kwargs):

		if self.Actualizar_Script:
			vlan = self.Nap.Spliiter_principal.VLAN
			ip = vlan.ips.filter(cliente__isnull=True).first()
			if not self.IP or (self.IP.Vlan is not vlan):
				self.IP = ip
			puerto = self.Nap.Spliiter_principal.Numero_Puerto
			Tarjeta= self.Nap.Spliiter_principal.Tarjeta.Numero_Tarjeta
			LineProfile=self.Nap.Spliiter_principal.VLAN.LineProfile
			ServiceProfile=self.Nap.Spliiter_principal.VLAN.ServicePort
			script = f'ont add {Tarjeta} {puerto} sn-auth "{self.Sn_auth}" omci ont-lineProfile-id {LineProfile} ont-srvprofile-id {ServiceProfile} des \'{self.Nombre} \''
			self.Script = script
			self.Actualizar_Script=False
		else:
			self.Script = ""
		super().save(*args, *kwargs)

	def __str__(self):
		valor = f"{self.Nombre }"
		return valor



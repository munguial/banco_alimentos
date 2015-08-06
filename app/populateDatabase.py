# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from database_setup import Base, Institution, Contact, TagName, Tag

engine = create_engine(os.environ["DATABASE_URL"])
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



test_inst1 = Institution(name="Banco de alimentos", address="Rinconada del Agua Nº 2811, Colonia Rinconada del Bosque, C.P. 44530, Guadalajara, Jalisco", description="Asociación civil mexicana sin fines de lucro que opera desde 1995 y se dedica al rescate de alimento para combatir el hambre y mejorar la nutrición de la población vulnerable en México.", telephone1="3331620330", telephone2="8000102622", email="", url="institucion1.com")
session.add(test_inst1)

test_inst2 = Institution(name="Institucion de prueba 2", address="calle 1 colonia 2", description="esta es una institucion de prueba", telephone1="3325487456", telephone2="32546898745", email="institucion2@prueba.com", url="http://bancosdealimentos.org.mx/")
session.add(test_inst2)

test_inst3 = Institution(name="Institucion de prueba 3", address="calle 1 colonia 2", description="esta es una institucion de prueba", telephone1="3325487456", telephone2="32546898745", email="institucion3@prueba.com", url="institucion3.com")
session.add(test_inst3)

test_inst4 = Institution(name="Institucion de prueba 4", address="calle 1 colonia 2", description="esta es una institucion de prueba", telephone1="3325487456", telephone2="32546898745", email="institucion4@prueba.com", url="institucion4.com")
session.add(test_inst4)

test_inst5 = Institution(name="Institucion de prueba 5", address="calle 1 colonia 2", description="esta es una institucion de prueba", telephone1="3325487456", telephone2="32546898745", email="institucion5@prueba.com", url="institucion5.com")
session.add(test_inst5)

contact1 = Contact(institution=test_inst1, name="Banco de Alimentos de Morelia", latitude=19.720515, longitude=-101.166866, address="Felipe Paramo #600 Col. Constituyentes de Querétaro, C.P. 58219, Morelia, Mich.", telephone1="4433230107", telephone2="4433230292", url="http://www.bamorelia.org.mx/", email="comunicacion@bamorelia.org.mx", notas="El Banco de Alimentos inicia sus operaciones en la ciudad de Morelia bajo la iniciativa del Excmo. Sr. Arzobispo Alberto Suárez y empresarios de la ciudad de Morelia, realizando la función de acopio, selección y distribución de alimento (perecedero y no perecedero) entregado en donación para hacerlo llegar en forma organizada a las zonas urbanas y conurbadas marginadas de Morelia, fungiendo como un puente entre aquellos que tienen y los que más necesitan.")
session.add(contact1)

contact2 = Contact(institution=test_inst1, name="Alimento para los más necesitados de León, A.C.", latitude=21.088959, longitude=-101.644865, address="Boulevard Miguel de Cervantes Saavedra No.8701-A, Col. Colinas de Santa Julia, C.P. 36530, León, Gto.", telephone1="4777727990", telephone2="4777727991", url="http://www.bancodealimentosleon.org.mx/", email="logistica@bancodealimentosleon.org.mx",  notas="Nuestra labor implica la atención alimentaria de niños, adultos mayores, jóvenes y mujeres amas de casa que carecen de los recursos económicos mínimos y suficientes para satisfacer las necesidades básicas de sus familias.")
session.add(contact2)

contact3 = Contact(institution=test_inst1, name="Banco de Alimentos de Veracruz", latitude=19.176941, longitude= -96.154438, address="Calle 16 864 Pocitos y Rivera 91729 Veracruz, Ver.", telephone1="2291781714", telephone2="2291781743", url="http://www.bav.org.mx/", email="COMUNICACION@BAV.ORG.MX",  notas="Contribuir a reducir el hambre y la desnutrición, distribuyendo adecuadamente productos alimenticios que donan productores, comerciantes y personas altruistas, para alcanzar la promoción humana en los aspectos personal, espiritual y comunitario.")
session.add(contact3)

contact4 = Contact(institution=test_inst1, name="Hogar de la Misericordia de Torreón AC", latitude=20.506119, longitude=-103.170030, address="Av Torre Latino 1000 Residencial las Torres Sector I, C.P. 27085, Torreón, Coah.", telephone1="6621188152", telephone2="6622607203", url="http://www.oscscoahuila.mx/banco-de-alimentos-de-saltillo-ac", email="hmisericordiat_2010@hotmail.com",  notas="Combatir el hambre, recuperando los productos que son regularmente desperdiciados por estar ligeramente dañados en su presentación pero en buenas condiciones de consumo, haciéndolos llegar a la gente necesitada a través de instituciones de beneficencia y/o directamente por centros de distribución del Banco de Alimentos de Saltillo.")
session.add(contact4)

contact5 = Contact(institution=test_inst3, name="contacto 5", latitude=18.539734, longitude=-99.554679, address="Juliantla, Gro.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com",  notas="punto de contacto de la institucion de prueba 3")
session.add(contact5)

contact6 = Contact(institution=test_inst3, name="contacto 6", latitude=20.672569, longitude=-102.570216, address="Calle Pedro Moreno 146A, San José de Gracia, Jal.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com", notas="punto de contacto de la institucion de prueba 3")
session.add(contact6)

contact7 = Contact(institution=test_inst4, name="contacto 7", latitude=22.145660, longitude=-102.412831, address="Juan Hernández Loera 309, 20500 San José de Gracia, Ags.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com",  notas="punto de contacto de la institucion de prueba 4")
session.add(contact7)

contact8 = Contact(institution=test_inst4, name="contacto 8", latitude=21.924705, longitude=-102.283652, address="Pozo del Oro 112, Aguascalientes, Ags.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com",  notas="punto de contacto de la institucion de prueba 4")
session.add(contact8)

contact9 = Contact(institution=test_inst5, name="contacto 9", latitude=21.878277, longitude=-102.249852, address="Las Cumbres 701, Aguascalientes, Ags.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com",  notas="punto de contacto de la institucion de prueba 5")
session.add(contact9)

contact10 = Contact(institution=test_inst5, name="contacto 10", latitude=20.709214, longitude=-103.410084, address="cartelera, Real de Acueducto, Puerta de Hierro, 45116 Zapopan, Jal.", telephone1="3325487456", telephone2="32546898745", url="hola.com", email="hola@hola.com",  notas="punto de contacto de la institucion de prueba 5")
session.add(contact10)


tag_name1 = TagName(name="Agua")
session.add(tag_name1)

tag_name2 = TagName(name="Atención Psicológica")
session.add(tag_name2)

tag_name3 = TagName(name="Capacitación para el Trabajo")
session.add(tag_name3)

tag_name4 = TagName(name="Ciudadanía")
session.add(tag_name4)

tag_name5 = TagName(name="Contraloría social")
session.add(tag_name5)

tag_name6 = TagName(name="Desarrollo Humano")
session.add(tag_name6)

tag_name7 = TagName(name="Discapacidad")
session.add(tag_name7)

tag_name8 = TagName(name="Educación Financiera")
session.add(tag_name8)

tag_name9 = TagName(name="Educación Formal")
session.add(tag_name9)

tag_name10 = TagName(name="Electricidad")
session.add(tag_name10)

tag_name11 = TagName(name="Empleabilidad")
session.add(tag_name11)

tag_name12 = TagName(name="Empoderamiento")
session.add(tag_name12)

tag_name13 = TagName(name="Emprendimiento y crédito")
session.add(tag_name13)

tag_name14 = TagName(name="Equidad de Género")
session.add(tag_name14)

tag_name15 = TagName(name="Espacios Públicos")
session.add(tag_name15)

tag_name16 = TagName(name="Estabilidad Emocional")
session.add(tag_name16)

tag_name17 = TagName(name="Integración Familiar")
session.add(tag_name17)

tag_name18 = TagName(name="Nutrición")
session.add(tag_name18)

tag_name19 = TagName(name="Participación ciudadana")
session.add(tag_name19)

tag_name20 = TagName(name="Salud")
session.add(tag_name20)

tag_name21 = TagName(name="Seguridad")
session.add(tag_name21)

tag_name22 = TagName(name="Servicios básicos")
session.add(tag_name22)

tag_name23 = TagName(name="Servicios Públicos")
session.add(tag_name23)

tag_name24 = TagName(name="Tejido Social")
session.add(tag_name24)

tag_name25 = TagName(name="Vivienda")
session.add(tag_name25)

tag_name26 = TagName(name="Humanitarios")
session.add(tag_name26)

tag_name27 = TagName(name="Diversidad Sexual")
session.add(tag_name27)


tag1 = Tag(contact = contact1, tag_name = tag_name4)
session.add(tag1)

tag2 = Tag(contact = contact1, tag_name = tag_name4)
session.add(tag2)

tag3 = Tag(contact = contact2, tag_name = tag_name4)
session.add(tag3)

tag4 = Tag(contact = contact2, tag_name = tag_name5)
session.add(tag4)

tag5 = Tag(contact = contact3, tag_name = tag_name5)
session.add(tag5)

tag6 = Tag(contact = contact3, tag_name = tag_name3)
session.add(tag6)

tag7 = Tag(contact = contact3, tag_name = tag_name2)
session.add(tag7)

tag8 = Tag(contact = contact4, tag_name = tag_name2)
session.add(tag8)

tag9 = Tag(contact = contact5, tag_name = tag_name2)
session.add(tag9)

tag10 = Tag(contact = contact6, tag_name = tag_name1)
session.add(tag10)

tag11 = Tag(contact = contact6, tag_name = tag_name1)
session.add(tag11)


session.commit()

print "Records inserted."

# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Institution, Contact, TagName, Tag

engine = create_engine('postgresql://amunguia:@localhost/banco', encoding='utf-8')
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



test_inst1 = Institution(name="Institucion de prueba 1", address="calle 1 colonia 2", description="esta es una institucion de prueba")
session.add(test_inst1)

test_inst2 = Institution(name="Institucion de prueba 2", address="calle 1 colonia 2", description="esta es una institucion de prueba")
session.add(test_inst2)

test_inst3 = Institution(name="Institucion de prueba 3", address="calle 1 colonia 2", description="esta es una institucion de prueba")
session.add(test_inst3)

test_inst4 = Institution(name="Institucion de prueba 4", address="calle 1 colonia 2", description="esta es una institucion de prueba")
session.add(test_inst4)

test_inst5 = Institution(name="Institucion de prueba 5", address="calle 1 colonia 2", description="esta es una institucion de prueba")
session.add(test_inst5)



contact1 = Contact(institution=test_inst1, latitude=20.704702, longitude=-103.376477, address="De las Américas 1608, Country Club, 44610 Guadalajara, Jal.", notas="punto de contacto de la institucion de prueba 1")
session.add(contact1)

contact2 = Contact(institution=test_inst1, latitude=20.646173, longitude=-103.352513, address="Calle 5 179, 44440 Guadalajara, Jal.", notas="punto de contacto de la institucion de prueba 1")
session.add(contact2)

contact3 = Contact(institution=test_inst2, latitude=20.650698, longitude=-103.220313, address="Av de las Praderas, Rancho de La Cruz, Coyula, Jal.", notas="punto de contacto de la institucion de prueba 2") 
session.add(contact3)

contact4 = Contact(institution=test_inst2, latitude=20.506119, longitude=-103.170030, address="Juanacatlán Centro, Juanacatlán, Jal.", notas="punto de contacto de la institucion de prueba 2")
session.add(contact4)

contact5 = Contact(institution=test_inst3, latitude=18.539734, longitude=-99.554679, address="Juliantla, Gro.", notas="punto de contacto de la institucion de prueba 3")
session.add(contact5)

contact6 = Contact(institution=test_inst3, latitude=20.672569, longitude=-102.570216, address="Calle Pedro Moreno 146A, San José de Gracia, Jal.", notas="punto de contacto de la institucion de prueba 3")
session.add(contact6)

contact7 = Contact(institution=test_inst4, latitude=22.145660, longitude=-102.412831, address="Juan Hernández Loera 309, 20500 San José de Gracia, Ags.", notas="punto de contacto de la institucion de prueba 4")
session.add(contact7)

contact8 = Contact(institution=test_inst4, latitude=21.924705, longitude=-102.283652, address="Pozo del Oro 112, Aguascalientes, Ags.", notas="punto de contacto de la institucion de prueba 4")
session.add(contact8)

contact9 = Contact(institution=test_inst5, latitude=21.878277, longitude=-102.249852, address="Las Cumbres 701, Aguascalientes, Ags.", notas="punto de contacto de la institucion de prueba 5")
session.add(contact9)

contact10 = Contact(institution=test_inst5, latitude=20.709214, longitude=-103.410084, address="cartelera, Real de Acueducto, Puerta de Hierro, 45116 Zapopan, Jal.", notas="punto de contacto de la institucion de prueba 5") 
session.add(contact10)



tag_name1 = TagName(name="Salud")
session.add(tag_name1)

tag_name2 = TagName(name="Alimento")
session.add(tag_name2)

tag_name3 = TagName(name="Vivienda")
session.add(tag_name3)

tag_name4 = TagName(name="Trabajo")
session.add(tag_name4)

tag_name5 = TagName(name="Vestimenta")
session.add(tag_name5)



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
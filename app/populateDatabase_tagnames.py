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

print "Records inserted."

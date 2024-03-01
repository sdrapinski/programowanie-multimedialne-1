from OpenGL.GL import *
import glfw
import glm

from helpers.shaders import DemoShaders
from helpers.models import *

def init_opengl_program(window):
	# Czyszczenie okna na kolor czarny
	glClearColor(0, 0, 0, 1)

	# Ładowanie programów cieniujących
	DemoShaders.initShaders("helpers/shaders/")

sun = Sphere(.5)
earth = Sphere(.2)
moon = Sphere(.1)

earth2 = Sphere(.25)
moon2 = Sphere(0.07)

def draw_scene(window,time):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	V = glm.lookAt(
		glm.vec3(0.0, 0.0, -5.0),
		glm.vec3(0.0, 0.0, 0.0),
		glm.vec3(0.0, 1.0, 0.0)
	)
	P = glm.perspective(glm.radians(50.0), 1.0, 1.0, 50.0)

	DemoShaders.spConstant.use()
	glUniformMatrix4fv(DemoShaders.spConstant.u("P"), 1, GL_FALSE, P.to_list())
	glUniformMatrix4fv(DemoShaders.spConstant.u("V"), 1, GL_FALSE, V.to_list())

	M = glm.mat4(1.0)
	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, M.to_list())

	sun.drawWire()
	## earth
	mEarth = glm.mat4(1.0)
	mEarth *= glm.rotate(glm.radians(60)*time, glm.vec3(0, 1, 0))
	mEarth *= glm.translate(glm.vec3(1.5, 0, 0))

	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, mEarth.to_list())
	earth.drawSolid()

	## moon
	mMoon = mEarth
	mMoon *= glm.rotate(glm.radians(60)*time, glm.vec3(0, 1, 0))
	mMoon *= glm.translate(glm.vec3(.5, 0, 0))
	
	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, mMoon.to_list())
	moon.drawSolid()
	# Earth 2

	mEarth2 = M
	mEarth2 *= glm.rotate(glm.radians(60)*time, glm.vec3(0, 0, 1))
	mEarth2 *= glm.translate(glm.vec3(0, 2, 1))

	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, mEarth2.to_list())
	earth2.drawSolid()

	#Moon 2
	mMoon2 = mEarth2
	mMoon2 *= glm.rotate(glm.radians(60)*time, glm.vec3(0, 1, 0))
	mMoon2 *= glm.translate(glm.vec3(.5, 0, 0))
	
	glUniformMatrix4fv(DemoShaders.spConstant.u("M"), 1, GL_FALSE, mMoon2.to_list())
	moon2.drawSolid()


	glfw.swap_buffers(window)

def free_opengl_program(window):
	# Możesz dodać odpowiednie czyszczenie zasobów tutaj, jeśli jest to konieczne
	pass

def main():
	glfw.init()
	window = glfw.create_window(500, 500, "Programowanie multimedialne", None, None)
	glfw.make_context_current(window)
	glfw.swap_interval(1)

	init_opengl_program(window)

	glfw.set_time(0)

	while not glfw.window_should_close(window):
		draw_scene(window,glfw.get_time())
		glfw.poll_events()

	free_opengl_program(window)
	glfw.terminate()


if __name__ == "__main__":
	main()

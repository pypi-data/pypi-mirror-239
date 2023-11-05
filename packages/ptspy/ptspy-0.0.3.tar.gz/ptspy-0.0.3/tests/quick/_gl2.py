from ptspy import Pt, Form
import glfw

# Not working yet
# Testing this: https://github.com/kyamagu/skia-python/issues/97


def main():
    # window = Form.createGLWindow(width, height)
    form = Form.setupGL(200, 200)

    def render(window):
        form.clear(0xFFCCAA)
        form.draw_point(Pt(100, 100), 0x0000FF, 20)
        form.surface().flushAndSubmit()

    Form.renderGL(form.window, render)


if __name__ == "__main__":
    main()

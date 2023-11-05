from ptspy import Pt, Form
import glfw
from OpenGL import GL
import skia

# Not working yet
# Testing this: https://github.com/kyamagu/skia-python/issues/97


width, height = 200, 200


def init_surface(width, height):
    context = skia.GrDirectContext.MakeGL()
    backend_render_target = skia.GrBackendRenderTarget(
        width, height, 0, 0, skia.GrGLFramebufferInfo(0, GL.GL_RGBA8)  # sample count  # stencil bits
    )
    surface = skia.Surface.MakeFromBackendRenderTarget(
        context,
        backend_render_target,
        skia.kBottomLeft_GrSurfaceOrigin,
        skia.kRGBA_8888_ColorType,
        skia.ColorSpace.MakeSRGB(),
    )
    assert surface, "Failed to create a surface"
    return surface


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(width, height, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    surface = init_surface(width, height)
    canvas = surface.getCanvas()
    form = Form(canvas)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        glfw.wait_events()

        # Render here
        canvas.clear(skia.ColorGREEN)
        canvas.drawCircle(100, 100, 40, skia.Paint(Color=skia.ColorRED))
        form.draw_point(Pt(100, 100), 0x00FF, 20)
        canvas.getSurface().flushAndSubmit()

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

.. _LÖVE: http://www.love2d.org/
.. _Lua: http://www.lua.org/
.. _PyGame: http://www.pygame.org/


Kundalini
=========

LÖVE_ is an **awesome** framework you can use to make 2D games in Lua_,
in a very similar way with PyGame_.

Kundalini intends to offer an API similar to that of LÖVE to develop
games using PyGame.


Usage
-----

Subclass ``kundalini.FrameManager`` and override the method::
    @abstractmethod
    def build_screen(self) -> Surface:
        pass


It must return a ``pygame.surface.Surface``, like, for example, the
object returned by ``pygame.display.set_mode()``.

You also can override::
    def load(self) -> None:
        pass


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))


    def handle_event(self, event:Event) -> None:
        pass


    def update(self, delta:float) -> None:
        pass


The method ``load()`` is performed by ``init()`` call, just after
``pygame.init()``.

The method ``draw()`` is performed every drawing loop.

The method ``handle_event()`` is performed for each occuring event. It
receives the event as parameter.

The method ``update()`` is performed about 1024 times a second, and
receives the time delta in seconds since last performing as parameter.

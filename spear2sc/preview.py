import supriya
from supriya.osc import ThreadedOscProtocol, HealthCheck
from supriya.querytree import QueryTreeGroup, QueryTreeSynth
from supriya.synthdefs import Envelope
from supriya.ugens import EnvGen, SinOsc, Line

from .spear_utils import get_durations


def partial_ugen_builder(partials):
    builder = supriya.synthdefs.SynthDefBuilder("heck", parameter=0.5)
    with builder:
        ttl = Line.ar(start=0.0, stop=1.0, duration=4.0, done_action=2)
        amp_env = list(map(lambda partial: EnvGen.ar(envelope=Envelope(list(map(lambda p: p[2], partial)), get_durations(partial))), partials))
        freq_env = list(map(lambda partial: EnvGen.ar(envelope=Envelope(list(map(lambda p: p[1], partial)), get_durations(partial))), partials))
        sines = [(SinOsc.ar(freq_env[i], 0) * amp_env[i]) for i in range(len(amp_env) - 1)]
        mix = supriya.ugens.Mix.new(sines)
        out = supriya.ugens.Out.ar(bus=0, source=[mix] * 2)

    return builder.build(name="mix1", optimize=False)


class ServerOfHell(supriya.Server):
    def _connect(self):
        print("Evil will always find you....")
        self._osc_protocol = ThreadedOscProtocol()
        self._osc_protocol.connect(
            ip_address=self.ip_address,
            port=self.port,
            healthcheck=HealthCheck(
                request_pattern=["/status"],
                response_pattern=["/status.reply"],
                callback=self._shutdown,
                max_attempts=5,
                timeout=1.0,
                backoff_factor=1.5,
            ),
        )
        self._is_running = True
        self._setup_osc_callbacks()
        # self._setup_notifications()
        self._client_id = 1
        self._setup_allocators()
        self._setup_proxies()
        if self.client_id == 0:
            self._setup_default_groups()
            self._setup_system_synthdefs()
        self._servers.add(self)

    def _rehydrate(self):
        from supriya.realtime import Group, Synth

        def recurse(query_tree_node, node):
            for query_tree_child in query_tree_node.children:
                if isinstance(query_tree_child, QueryTreeGroup):
                    group = Group()
                    group._register_with_local_server(
                        node_id=query_tree_child.node_id, server=self
                    )
                    node._children.append(group)
                    recurse(query_tree_child, group)
                elif isinstance(query_tree_child, QueryTreeSynth):
                    synth = Synth()
                    synth._register_with_local_server(
                        node_id=query_tree_child.node_id, server=self
                    )
                    node._children.append(synth)

        recurse(self.query(), self.root_node)


def preview(partials):
    # supriya.Server().connect(ip_address="127.0.0.1", port=57110).reset().add_synthdef(partial_ugen_builder(partials)).disconnect()
    server = ServerOfHell().connect(ip_address="127.0.0.1", port=57110)
    print(server
          .add_synth(partial_ugen_builder(partials)))
    server.disconnect()

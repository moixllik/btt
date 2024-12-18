VER=$(shell cat ./version.txt)
DEMO=$(shell realpath ./demo.blend)

build: update
	@zip btt-$(VER).zip ./__init__.py ./blender_manifest.toml

update:
	@sed -i 's/version = "0.0.0"/version = "$(VER)"/g' ./blender_manifest.toml

server:
	@python3 -m http.server -d ./docs/

demo:
	@flatpak run org.blender.Blender $(DEMO)

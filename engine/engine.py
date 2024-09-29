#
# Simple implementation of a 2D dungeon crawler render.
# This loads atlases generated using the AtlasMaker (https://github.com/zooperdan/AtlasMaker-for-2D-Dungeon-Crawlers)
#
# Written by zooperdan
#
import json

from pygame import SRCALPHA, Surface, image, transform
from pygame.math import Vector2
from pygame.rect import Rect
from math import sin, cos, radians

from engine.atlasData import AtlasData
from engine.inputEventKey import InputEventKey
from engine.map import Map
from engine.party import Party
from engine.screenDimensions import ScreenDimensions

class Engine:

	def __init__(self, screen: Surface):
		self.screenSurface = screen
		self.screenDimensions = ScreenDimensions(320, 256)
		self.atlasData = None
		self.atlasTexture = None

		self.party = Party(2,1,1)

		self.map = Map(8, 8)
		self.map.squares = [
			[1,1,1,1,1,1,1,1],
			[1,0,0,0,1,0,0,1],
			[1,0,1,0,1,1,0,1],
			[1,0,0,1,0,0,0,1],
			[1,1,0,1,1,0,1,1],
			[1,0,0,0,0,0,1,1],
			[1,0,1,0,1,0,0,1],
			[1,1,1,1,1,1,1,1]
		]
		self.map.objects = [
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,1,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0]
		]
		self.map.doors = [
			[0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,1],
			[0,0,0,1,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[1,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,1,0,0,0,1,0,0]
		]

	def _ready(self):
		self.loadJSON()
		self.atlasTexture = image.load("res/atlases/atlas.png")
	
	def get_cropped_texture(self, texture, region):
		cropped_texture = Surface((region.width, region.height), SRCALPHA)
		cropped_texture.blit(texture, (0, 0), region)
		return cropped_texture
	
	def loadJSON(self):

		with open('res/atlases/atlas.json', 'r') as file:
			data = json.load(file)

			self.atlasData = AtlasData(
							  data['version'], 
							  data['generated'], 
							  data['resolution'],
							  data['depth'],
							  data['width']) 
	
			for i in range(0, len(data['layers'])):
				self.atlasData.layers[data['layers'][i]['name']] = data['layers'][i]
			

	def _input(self, event: InputEventKey):
		if event.pressed:
			if event.is_action_pressed("forward"):
				self.moveForward()
			if event.is_action_pressed("backward"):
				self.moveBackward()
			if event.is_action_pressed("strafe_left"):
				self.strafeLeft()
			if event.is_action_pressed("strafe_right"):
				self.strafeRight()
			if event.is_action_pressed("turn_left"):
				self.turnLeft()
			if event.is_action_pressed("turn_right"):
				self.turnRight()

	def _draw(self):
		self.renderDungeon()
			
	def _process(self, delta):
		# self.queue_redraw()	
		pass
	
	def canMove(self, pos: Vector2):
		
		# can't move through walls
		if self.map.squares[int(pos.y)][int(pos.x)] == 1:
			return False

		# can't step over chests
		if self.map.objects[int(pos.y)][int(pos.x)] == 1:
			return False
		
		return True

	def invertDirection(self, direction:int):
		if direction == 0: return 2
		if direction == 1: return 3
		if direction == 2: return 0
		if direction == 3: return 1

	def getDestPos(self, direction:int):
		
		vec = Vector2(
			sin(radians(direction*90)),
			-cos(radians(direction*90))
		)

		vec.x = vec.x + self.party.x
		vec.y = vec.y + self.party.y
		
		return vec
				
	def moveForward(self):

		destPos = self.getDestPos(self.party.direction)

		if self.canMove(destPos):
			self.party.x = destPos.x
			self.party.y = destPos.y
	
	def moveBackward(self):

		destPos = self.getDestPos(self.invertDirection(self.party.direction))

		if self.canMove(destPos):
			self.party.x = destPos.x
			self.party.y = destPos.y
		
	def strafeLeft(self):

		direction = self.party.direction - 1
		if direction < 0: direction = 3
		
		destPos = self.getDestPos(direction)

		if self.canMove(destPos):
			self.party.x = destPos.x
			self.party.y = destPos.y		
	
	def strafeRight(self):

		direction = self.party.direction + 1
		if direction > 3: direction = 0
		
		destPos = self.getDestPos(direction)

		if self.canMove(destPos):
			self.party.x = destPos.x
			self.party.y = destPos.y		
			
	def turnLeft(self):
		self.party.direction = self.party.direction - 1
		if self.party.direction < 0:
			self.party.direction = 3
		
	def turnRight(self):
		self.party.direction = self.party.direction + 1
		if self.party.direction > 3:
			self.party.direction = 0
			
	def getPlayerDirectionVectorOffsets(self, x, z):

		if self.party.direction == 0:
			return Vector2(self.party.x + x, y = self.party.y + z)
		elif self.party.direction == 1:
			return Vector2(self.party.x - z, self.party.y + x)
		elif self.party.direction == 2:
			return Vector2(self.party.x - x, self.party.y - z)
		elif self.party.direction == 3:
			return Vector2(self.party.x + z, self.party.y - x)

	def getTileFromAtlas(self, layerId, tileType, x, z):

		if not self.atlasData.layers[layerId]: return None

		layer = self.atlasData.layers[layerId]
		
		if not layer: return False
		
		for i in range(0, len(layer['tiles'])):
			tile = layer['tiles'][i]
			if tile['type'] == tileType and tile['tile']['x'] == x and tile['tile']['y'] == z:
				return tile

		return None

	def drawFrontWalls(self, layerId, x, z):
		
		bothsides = self.atlasData.layers[layerId] and self.atlasData.layers[layerId]['mode'] == 2
		
		xx = x - (x * 2) if bothsides else 0
		tile = self.getTileFromAtlas(layerId, "front", xx, z)

		if tile:
			txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
			tx = tile['screen']['x'] + (x * tile['coords']['w'])
			self.draw_set_transform(txt, Vector2(tx, tile['screen']['y']), 0, Vector2(1,1))
			# self.draw_texture(txt, Vector2(0,0))
		
	def drawSideWalls(self, layerId, x, z):

		if x <= 0:
			tile = self.getTileFromAtlas(layerId, "side", x - (x * 2), z)
			if tile:
				txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
				self.draw_set_transform(txt, Vector2(tile['screen']['x'], tile['screen']['y']), 0, Vector2(1,1))
				# self.draw_texture(txt, Vector2(0,0))

		if x >= 0:
			tile = self.getTileFromAtlas(layerId, "side", x, z)
			if tile:
				txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
				tx = self.screenDimensions.width - tile['screen']['x']
				self.draw_set_transform(txt, Vector2(tx, tile['screen']['y']), 0, Vector2(-1,1))
				# self.draw_texture(txt, Vector2(0,0))
	
	def drawObject(self, layerId, x, z):

		bothsides = self.atlasData.layers[layerId] and self.atlasData.layers[layerId]['mode'] == 2
		
		xx = x - (x * 2) if bothsides else 0
		tile = self.getTileFromAtlas(layerId, "object", xx, z)

		if tile:
			txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
			self.draw_set_transform(txt, Vector2(tile['screen']['x'], tile['screen']['y']), 0, Vector2(1,1))
			# self.draw_texture(txt, Vector2(0,0))

	def drawFrontDoors(self, layerId, x, z):
		
		xx = x - (x * 2)
		tile = self.getTileFromAtlas(layerId, "front", xx , z)

		if tile:
			txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
			tx = tile['screen']['x'] + (x * tile['coords']['w'])
			self.draw_set_transform(txt, Vector2(tx, tile['screen']['y']), 0, Vector2(1,1))
			# self.draw_texture(txt, Vector2(0,0))
			
	def drawSideDoors(self, layerId, x, z):

		if x <= 0:
			tile = self.getTileFromAtlas(layerId, "side", x - (x * 2), z)
			if tile:
				txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
				self.draw_set_transform(txt, Vector2(tile['screen']['x'], tile['screen']['y']), 0, Vector2(1,1))
				# self.draw_texture(txt, Vector2(0,0))

		if x >= 0:
			tile = self.getTileFromAtlas(layerId, "side", x, z)
			if tile:
				txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
				tx = self.screenDimensions.width - tile['screen']['x']
				self.draw_set_transform(txt, Vector2(tx, tile['screen']['y']), 0, Vector2(-1,1))
				# self.draw_texture(txt, Vector2(0,0))
						
	def drawMapCell(self, x, z):

		p = self.getPlayerDirectionVectorOffsets(x, z)

		if p.x >= 0 and p.y >= 0 and p.x < self.map.width and p.y < self.map.height:
			if self.map.squares[int(p.y)][int(p.x)] == 1:
				self.drawSideWalls("wall", x, z)
				self.drawFrontWalls("wall", x, z)
			if self.map.doors[int(p.y)][int(p.x)] != 0:
				self.drawFrontDoors("door", x, z)
				self.drawSideDoors("door", x, z)
			if self.map.objects[int(p.y)][int(p.x)] != 0:
				self.drawObject("object", x, z)

	def drawBackground(self, layerId):
		
		bothsides = self.atlasData.layers[layerId] and self.atlasData.layers[layerId]['mode'] == 2

		for z in range(-self.atlasData.depth, 1):

			for x in range(-self.atlasData.width, self.atlasData.width):

				xx = x - (x * 2) if bothsides else 0
				tile = self.getTileFromAtlas(layerId, layerId, xx, z)
				
				if tile:
					txt = self.get_cropped_texture(self.atlasTexture, Rect(tile['coords']['x'], tile['coords']['y'], tile['coords']['w'], tile['coords']['h']))
					self.draw_set_transform(txt, Vector2(tile['screen']['x'], tile['screen']['y']), 0, Vector2(1,1))
					# self.draw_texture(txt, Vector2(0,0))
					

	def renderDungeon(self):
		
		self.drawBackground("ground")
		self.drawBackground("ceiling")
			
		for z in range(-self.atlasData.depth, 1):
			for x in range(-self.atlasData.width, 0):
				self.drawMapCell(x, z)
			for x in range(self.atlasData.width, 0, -1):
				self.drawMapCell(x, z)
			self.drawMapCell(0, z)

	def draw_set_transform(self, 
						   image: Surface,
						   position: Vector2, 
						   rotation: float = 0.0, 
						   scale: Vector2 = Vector2(1, 1)):

		# Flip the image if scale.x or scale.y is negative
		flipped_image = transform.flip(image, scale[0] < 0, scale[1] < 0)

		# Scale the image
		scaled_image = transform.scale(flipped_image, (abs(int(image.get_width() * scale[0])), abs(int(image.get_height() * scale[1]))))
		
		# Rotate the image
		rotated_image = transform.rotate(scaled_image, rotation)
		
		# Get the rect of the rotated image
		if (scale[0] > 0):
			rect = rotated_image.get_rect(topleft=position)
		else:
			rect = rotated_image.get_rect(topright=position)

		# Draw the transformed image
		self.screenSurface.blit(rotated_image, rect.topleft)

	# def draw_texture(self, texture: Surface, position: Vector2):
	# 	self.screenSurface.blit(texture, position)
from PIL import Image
import pytesseract as tess


class CaptchaSolver:
	white_pixel = (255, 255, 255)
	black_pixel = (0, 0, 0)
	def __init__(self, tesseract_path):
		tess.pytesseract.tesseract_cmd = tesseract_path

	def rgb_to_hsv(self, r, g, b):
		"""
		This converts an rgb pixel to hsv
		I have no clue how it works
		"""
		r, g, b = r / 255.0, g / 255.0, b / 255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		df = mx - mn
		if mx == mn:
			h = 0
		elif mx == r:
			h = (60 * ((g - b) / df) + 360) % 360
		elif mx == g:
			h = (60 * ((b - r) / df) + 120) % 360
		elif mx == b:
			h = (60 * ((r - g) / df) + 240) % 360
		if mx == 0:
			s = 0
		else:
			s = (df / mx) * 100
		v = mx * 100
		return h, s, v

	def is_dark(self, color):
		"""
		Determines if a pixel is dark by looking at its V value in hsv,
		and saying that if v is low, it's dark

		:param color: tuple of (red, green, blue)
		:return: darkness boolean
		"""
		h, s, v = self.rgb_to_hsv(color[0], color[1], color[2])
		blackness_threshold = 22
		return v < blackness_threshold

	def is_light(self, color):
		"""
		Determines if a pixel is light by looking at its V value in hsv,
		and saying that if v is high, it's light

		:param color: tuple of (red, green, blue)
		:return: lightness boolean
		"""
		h, s, v = self.rgb_to_hsv(color[0], color[1], color[2])
		lightness_threshold = 70
		return v > lightness_threshold

	def remove_light(self, image, image_pixels):
		"""
		Removes all "light" pixels from the image according to is_light function
		Removed pixels are set to white

		:param image: An Image object
		:param image_pixels: The image.load() containing pixels
		"""
		img_width = image.size[0]
		img_length = image.size[1]
		for row in range(img_width):
			for col in range(img_length):
				current_pixel = image_pixels[row, col]
				if self.is_light(current_pixel):
					image_pixels[row, col] = CaptchaSolver.white_pixel

	def remove_dark(self, image, image_pixels):
		"""
		Removes all "dark" pixels from the image according to the is_dark function
		Also removes pixels surrounding the dark pixels in a 1 pixel distance
		"Removed" pixels are set to white

		:param image: An Image object
		:param image_pixels: The image.load() containing pixels
		"""
		img_width = image.size[0]
		img_length = image.size[1]
		for row in range(img_width):
			for col in range(img_length):
				if self.is_dark(image_pixels[row, col]):
					close_pixels = self.neighbor_array(image_pixels, row, col)
					for r, c in close_pixels:
						image_pixels[r, c] = CaptchaSolver.white_pixel
					image_pixels[row, col] = CaptchaSolver.white_pixel


	def darken_remaining(self, image, image_pixels):
		img_width = image.size[0]
		img_length = image.size[1]
		for row in range(img_width):
			for col in range(img_length):
				current_pixel = image_pixels[row, col]
				r, g, b = current_pixel[0], current_pixel[1], current_pixel[2]
				h, s, v = self.rgb_to_hsv(r, g, b)
				if v < 100:
					image_pixels[row, col] = CaptchaSolver.black_pixel

	def is_lonely(self, neighbors, image_pixels, loneliness = 2):
		black_count = 0
		for row, col in neighbors:
			if image_pixels[row, col] == CaptchaSolver.black_pixel:
				black_count += 1
		return black_count < loneliness

	def remove_lonely(self, image, image_pixels):
		img_width = image.size[0]
		img_length = image.size[1]
		for row in range(img_width):
			for col in range(img_length):
				pixel_neighbors = self.neighbor_array(image_pixels, row, col)
				if self.is_lonely(pixel_neighbors, image_pixels):
					"""
					lonely_neighbors = 0
					for r, c in pixel_neighbors:
						neighbor_neighbors = self.neighbor_array(image_pixels, r, c, reach=1)
						if not self.is_lonely(neighbor_neighbors, image_pixels, loneliness=1):
							lonely_neighbors += 1
					if lonely_neighbors > 0:
					"""
					image_pixels[row, col] = CaptchaSolver.white_pixel

	def neighbor_array(self, image_pixels, row, column, reach = 1):
		"""

		:param image_pixels: The array of image pixels
		:param row: The row of the pixel in question
		:param column: The column of the pixel in question
		:return: An array like [(2, 3), (3,3), (3,4)] etc that is just a
		3x3 square centered about the test pixel. This function is error-safe for indices
		"""
		array = []
		for r in range((row - reach), row + (reach + 1), 1):
			# Same for column
			for c in range(column - (reach), column + (reach + 1), 1):
				if (r, c) == (row, column):
					continue
				try:
					# We will try to index image_pixels at r, c, and if there is an index error,
					# We will just ignore it and not add it to the array
					test = image_pixels[r, c]
					array.append((r, c))
				except IndexError:
					continue
		return array

	def resolve(self, captcha_path):
		"""

		:param captcha_path: The path to your TypeRacer Captcha
		:return: a string representing the solved captcha
		"""
		captcha = Image.open(captcha_path)
		# Captcha.load() will return an object which stores pixels at [r,c]
		# So we store this value
		captcha_pixels = captcha.load()
		self.remove_light(captcha, captcha_pixels)
		self.remove_dark(captcha, captcha_pixels)
		#captcha.save("fixed-captcha.png")
		self.darken_remaining(captcha, captcha_pixels)
		self.remove_lonely(captcha, captcha_pixels)
		# Remove this line to save time. It's just meant for testing by looking at the fixed captcha
		#captcha.save("fixed-captcha2.png")

		whitelist = " .,;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		solution = tess.image_to_string(captcha, lang="eng", config = r"-c tessedit_char_whitelist= .,;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		return solution



if __name__ == '__main__':
	solver = CaptchaSolver("C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
	solution = solver.resolve("captcha_image.png")
	print(solution)

import tkinter as tk
import math

class PlottingApp(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.create_widgets()

	def create_widgets(self):
		self.lbl_prompt = tk.Label(text = "Input your data in the box below")
		self.lbl_prompt.grid(row=0, column=0)

		self.txt_user = tk.Text()
		self.txt_user.grid(row=1, column=0)

		self.btn_submit = tk.Button(text= "Submit", command=self.handle_click)
		self.btn_submit.grid(row=0, column=1)

		self.canvas_plot = tk.Canvas(bg='white')
		self.canvas_plot.grid(row=1, column=2)

	def handle_click(self):
		#clear canvas
		self.user_input = self.txt_user.get("1.0", tk.END)
		self.points = self.format_input()
		self.make_plot()

	def format_input(self):
		#header
		rows = self.user_input.splitlines()
		x_coords = set()
		y_coords = set()
		pts = {}
		for r in rows:
			columns = r.split(',')
			assert len(columns) == 4, "Each row must have 4 columns"

			category = columns[0].strip()
			try:
				x = float(columns[2])
			except:
				print("X column must only have numbers")
				raise

			try:
				y = float(columns[3])
			except:
				print("Y column must only have numbers")
				raise

			x_coords.add(x)
			y_coords.add(y)

			if category in pts:
				pts[category].append((x,y))
			else:
				pts[category] = [(x,y)]
		self.input_ranges = [min(x_coords), max(x_coords),min(y_coords), max(y_coords)]
		return pts

	def make_plot(self):
		#category colors
		#point uniqueness?
		#labels
		#legend
		circle_radius = 3
		sw_buffer = 50
		ne_buffer = 58
		axes_buffer = 8
		ZERO = 0

		width = int(self.canvas_plot['width'])
		height = int(self.canvas_plot['height'])

		min_x = self.input_ranges[0]
		max_x = self.input_ranges[1]
		min_y = self.input_ranges[2]
		max_y = self.input_ranges[3]

		x_scale_factor = (width - ne_buffer)/(max_x - min_x)
		y_scale_factor = (height - ne_buffer)/(max_y - min_y)

		#y_axis
		self.canvas_plot.create_line(sw_buffer- axes_buffer,ZERO,sw_buffer- axes_buffer,height - sw_buffer + axes_buffer)
		#x_axis
		self.canvas_plot.create_line(sw_buffer - axes_buffer,height - sw_buffer + axes_buffer, width, height - sw_buffer + axes_buffer)

		for category in self.points:
			for point in self.points[category]:
				x = (point[0] - min_x)*x_scale_factor + sw_buffer
				y = height - ((point[1] - min_y)*y_scale_factor + sw_buffer)
				
				self.canvas_plot.create_oval(x-circle_radius, 
					y-circle_radius,
					x+circle_radius, 
					y+circle_radius,
					fill='red')



root = tk.Tk()
app = PlottingApp(root)
app.master.title('Plotting Application')
app.mainloop()
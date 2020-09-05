<!DOCTYPE html>
<!-- By Santanu Sikder -->
<html>
	<head>
		<title>SS Line Equation Finder</title>
		
		<meta charset="utf-8"/>
		<meta name="description" content="A GUI based tool to find the equation of a line. It can be helpful for mathematical tasks as well as in Machine Learning (regression)."/>
		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
		
		<style>
			body{
				margin: 0;
			}
			
			#canvas-container{
				position: absolute;
				top: 1vw;
				left: 1vw;
				width: 96vw;
				height: 96vw;
				border: 1vw solid blue;
				overflow: scroll;
			}
			
			#canvas-container::-webkit-scrollbar{
				display: none;
			}
			
			canvas{
				position: absolute;
				width: 500%;
				height: 500%;
				background: black;
			}

			#controls{
				position: absolute;
				top: 100vw;
				left: 1vw;
				width: 96vw;
				height: calc(100% - 80vw);
				text-align: center;
				border: 1vw solid blue;
			}

			#output{
				width: 90%;
				height: 30px;
				background: red;
				color: white;
				text-align: center;
				font-weight: bold;
				font-size: 1.2rem;
				border-radius: 15px;
			}

			.small-input{
				width: 12%;
				text-align: center;
			}
			
			@media (orientation: landscape){
				#canvas-container{
					top: 1vh;
					left: 1vh;
					width: 96vh;
					height: 96vh;
					border: 1vh solid blue;
				}

				#controls{
					top: 1vh;
					left: 100vh;
					width: calc(100% - 103vh);
					height: 96vh;
					border: 1vh solid blue;
				}
			}
		</style>
	</head>
<!-- By Santanu Sikder -->
	<body>
		<div id="canvas-container">
			<canvas>
				Sorry, your browser doesn't support HTML5 Canvas.
			</canvas>
		</div>

		<div id="controls">
			Equation of the line:
			<br/>
			<input type="text" id="output" value="y = x" disabled/>
			<br/>
			<br/>
			<button onclick="centerOrigin()">(0, 0)</button> | <b>Passing point:</b> ( <input type="number" id="passing-point-x" class="small-input" value="0" onchange="updatePassingPointx(this.value)"/>, <input type="number" id="passing-point-y" class="small-input" value="0" onchange="updatePassingPointy(this.value)"/> )
			<br/>
			<br/>
			<b>Scale (0.1 - 100)</b> <input type="number" id="scale-input" class="small-input" value="1.0" onchange="updateScale(this.value)"/>
			<br/>
			<br/>
			<button id="scale-range-minus" onclick="scaleMinusOne()">-</button> <input type="range" id="scale-input-range" min="0.1" value="1.0" max="100" onchange="updateScale(parseFloat(this.value))"/> <button id="scale-range-plus" onclick="scalePlusOne()">+</button>
			<br/>
			<br/>
			<b>Angle:</b> <button onclick="anglePlusOne()">&cularr;</button> <input type="number" id="angle-input" class="small-input" value="45" onchange="updateAngle(this.value)"/>&deg; <button onclick="angleMinusOne()">&curarr;</button>
			<br/>
			<br/>
			<b>Intercept:</b> <button id="intercept-minus" onclick="interceptMinusOne()">&darr;</button> <input type="number" id="intercept-input" class="small-input" value="0" onchange="updateIntercept(this.value)"/> <button id="intercept-plus" onclick="interceptPlusOne()">&uarr;</button> | <b>CPP:</b> <input id="centerPassingPoint" type="checkbox" checked="true"/>
		</div>
		
		<script>
			const canvasContainer = document.querySelector("#canvas-container"), canvas = document.querySelector("canvas"), c = canvas.getContext("2d");
			const output = document.querySelector("#output"), scaleInput = document.querySelector("#scale-input"), scaleRangeMinus = document.querySelector("#scale-range-minus"), scaleInputRange = document.querySelector("#scale-input-range"), scaleRangePlus = document.querySelector("#scale-range-plus"), passingPointx = document.querySelector("#passing-point-x"), passingPointy = document.querySelector("#passing-point-y"), angleInput = document.querySelector("#angle-input"), interceptMinus = document.querySelector("#intercept-minus"), interceptInput = document.querySelector("#intercept-input"), interceptPlus = document.querySelector("#intercept-plus");
			const pi = Math.PI;
			var scale = 1.0, size = 0;
			(window.innerWidth <= window.innerHeight) ? size = 0.96 * window.innerWidth : size = 0.96 * window.innerHeight;
			var canvasSize = 5 * size, unit = canvasSize / 20; // size is the size of the canvasContainer and canvasSize is that of the canvas. And each positive axis has 10 points, with the value of each successive point increasing by scale. The separation between any two successive points on any of the axes is unit.
			var passingPoint = [0, 0], angle = 45, slope = 1, intercept = 0;
			
			// Let's ask our canvas to abide by our sizing laws ;-P
			canvas.width = canvasSize;
			canvas.height = canvasSize;
			
			function scrollCanvas(pointx, pointy, offsetx = 0, offsety = 0){
				// This function scrolls the canvasContainer to the specified point, with an extra x and y shift from the top-left corner, called offsets.

				canvasContainer.scrollTo(pointx - offsetx, pointy - offsety);
			}
			
			function centerPoint(pointx, pointy){
				// This function displays the specified point at the center and rest of the content adjusts accordingly.

				scrollCanvas(pointx, pointy, size / 2, size / 2);
			}

			function centerOrigin(){
				centerPoint(canvasSize / 2, canvasSize / 2);
			}

			function getRealCoordinates(x = 0, y = 0){
				/* On paper, we are habitual of using the natural sign convention of having the up direction as +ve y and the down one as -ve y.
				But in case of JS, we have the reverse to be true.
				So this function helps to use the natural convention as well.
				It actually returns a point as an array with its items being its real coordinates (the ones from the top-left corner of the canvas, in pixels), from the Cartesian coordinates specified as the arguments of the function. */

				return [canvasSize / 2 + x, canvasSize / 2 - y];
			}
// By  Santanu Sikder
			function drawLine(x1, y1, x2, y2, color = "white", lineWidth = 2.5){
				c.strokeStyle = color;
				c.lineWidth = lineWidth;

				c.beginPath();
				c.moveTo(x1, y1);
				c.lineTo(x2, y2);
				c.stroke();
			}
			
			function drawAxes(){
				// x-axis
				drawLine(0, canvasSize / 2, canvasSize, canvasSize / 2);

				// y-axis
				drawLine(canvasSize / 2, 0, canvasSize / 2, canvasSize);
			}

			function labelPoint(pointx, pointy, x, y, textColor = "white", pointColor = "white", bgBox = false){
				// Labels the point at coordinates (x, y) from the origin, with the label (pointx, pointy).

				var text = "(" + (scale * pointx).toFixed(1) + ", " + (scale * pointy).toFixed(1) + ")";
				fromOrigin = getRealCoordinates(x, y);

				// If bgBox is set to true, draw a white box behind the label.
				if(bgBox){
					c.fillStyle = "white";
					c.fillRect(fromOrigin[0], fromOrigin[1], 6 * text.length, 20);
				}

				c.fillStyle = textColor;
				c.font = "12px Arial";

				c.fillText(text, fromOrigin[0] + text.length / 4, fromOrigin[1] + 15);

				c.moveTo(fromOrigin[0], fromOrigin[1]);
				c.fillStyle = pointColor;
				c.arc(fromOrigin[0], fromOrigin[1], 4, 0, 2 * pi);
				c.fill();
			}

			function clear(){
				c.clearRect(0, 0, canvasSize, canvasSize);
			}

			function labelPointsOnTheAxes(){
				// This labels some points on each of the axes, separated by unit and succeeding in value by scale.

				// First remove everything that already exists.
				clear();

				// Now draw the axes
				drawAxes();

				// The origin.
				labelPoint(0, 0, 0, 0);

				// Points on the x-axis and on the y-axis.
				for(var i = 1; i <= 10; i++){
					labelPoint(i, 0, i * unit, 0);  // +ve x
					labelPoint(-i, 0, -i * unit, 0);  // -ve x

					labelPoint(0, i, 0, i * unit);  // +ve y
					labelPoint(0, -i, 0, -i * unit);  // -ve y
				}
			}

			function Y(x){
				// This returns the y-coordinate on the line of the point whose x-coordinate is x.

				return slope * x + intercept;  // Because y = mx + c
			}

			function X(y){
				// This returns the x-coordinate on the line of the point whose y-coordinate is y.

				return (y - intercept) / slope;
			}

			function getIntercept(){
				// It returns the value of the intercept based on the formula c = y - mx.
				// We'll use the passing point's coordinates (x1, y1) to find it: c = y1 - m * x1.

				return passingPoint[1] - slope * passingPoint[0];
			}

			function drawTheOutputLine(){
				// First let's clear up the canvas (what I hate the most about HTML5 canvas) and redraw the axes and the points on it.
				labelPointsOnTheAxes();

				var equation = "";  // This will hold the equation of the line.

				// If the line is horizontal.
				if(angle % 180 == 0){
					// First let's get the y-coordinate of the point on this line lying on the y-axis, and scale it up!
					var y = Y(0) * unit / scale;

					// Get the coordinates from the origin.
					var fromOrigin = getRealCoordinates(0, y);

					// Next, we'll use this y value to plot the horizontal line.
					drawLine(0, fromOrigin[1], canvasSize, fromOrigin[1], "yellow", 2);

					equation = "y = " + intercept;
				}
				// If the line is vertical.
				else if(angle % 90 == 0){
					// In case of a vertical line, let the intercept act as the x-intercept instead.
					var x = intercept * unit / scale;

					// Get the coordinates from the origin.
					var fromOrigin = getRealCoordinates(x, 0);

					// Plot the vertical line.
					drawLine(fromOrigin[0], 0, fromOrigin[0], canvasSize, "yellow", 2);

					equation = "x = " + intercept;
				}
				// But if we have a decent (inclined) line, just plot it down!
				else{
					var remainder = angle % 180;  // Remember, when a negative number is divided by a positive the remainder is negative.

					// If the line is inclined more toward the x-axis, or equally inclined on both the axes.
					if((remainder <= 45 && remainder >= -45) || remainder >= 135 || remainder <= -135){
						// The leftmost point of the output line on the canvas.
						var fromOrigin1 = getRealCoordinates(-10 * unit, Y(-10 * scale) * unit / scale);
						// The rightmost one.
						var fromOrigin2 = getRealCoordinates(10 * unit, Y(10 * scale) * unit / scale);

						drawLine(fromOrigin1[0], fromOrigin1[1], fromOrigin2[0], fromOrigin2[1], "yellow", 2);
					}
					// If the line is inclined more toward the y-axis.
					else{
						// The bottommost point of the output line on the canvas.
						var fromOrigin1 = getRealCoordinates(X(-10 * scale) * unit / scale, -10 * unit);
						// The topmost one.
						var fromOrigin2 = getRealCoordinates(X(10 * scale) * unit / scale, 10 * unit);

						drawLine(fromOrigin1[0], fromOrigin1[1], fromOrigin2[0], fromOrigin2[1], "yellow", 2);
					}

					equation = "y = ";

					if(remainder == 45 || remainder == -135)
						equation += "x";
					else if(remainder == 135 || remainder == -45)
						equation += "-x";
					else
						equation += slope + " * x";

					// For using proper spaces between the numbers and the signs, and also for not printing 0 as the intercept.
					if(intercept > 0)
						equation += " + " + intercept;
					else if(intercept < 0)
						equation += " - " + Math.abs(intercept);
				}

				// Label the passing point.
				labelPoint(passingPoint[0] / scale, passingPoint[1] / scale, unit * passingPoint[0] / scale, unit * passingPoint[1] / scale, "black", "yellow", true);

				// Outputs the equation
				output.value = equation;

				// Center the passing point, if CPP is checked and the point does not lie outside the canvas.
				if(document.querySelector("#centerPassingPoint").checked){
					// First let's get the real coordinates of the passing point.
					var x, y;
					[x, y] = getRealCoordinates(passingPoint[0] * unit / scale, passingPoint[1] * unit / scale);

					if(x > 0 && x < canvasSize && y > 0 && y < canvasSize)
						centerPoint(x, y);
				}
			}

			/*window.addEventListener("orientationchange", function(){
				// If an orientation change is detected, change the values of size, canvasSize and unit.
				// More precisely, if the new orientation is landscape then use the inner height to calculate all the above variables, else use the inner width.

				// First let's get the new orientation (angle of the screen assuming the normal portrait orientaion to be 0).
				var newOrientation = window.orientation;

				if(newOrientation == 0 || newOrientation == 180)
					size = 0.96 * window.innerWidth;
				else
					size = 0.96 * window.innerHeight;

				canvasSize = 5 * size;
				unit = canvasSize / 20;

				// Let's reassign the width and height of the canvas.
				canvas.width = canvasSize;
				canvas.height = canvasSize;

				// Redraw the output line.
				drawTheOutputLine();
			});*/
// By  Santanu Sikder
			function toRadians(angleInDegrees){
				return pi / 180 * angleInDegrees;
			}

			function toDegrees(angleInRadians){
				return 180 / pi * angleInRadians;
			}

			function getSlope(angleInRadians){
				// The conditions in which the slope becomes infinity have been handled separately in each such possible case.
				return Math.tan(angleInRadians).toFixed(2);
			}

			function updateScale(updatedValue){
				// Updates the value of scale to the given value (updatedValue).

				// Handle user's carelessness, when he/she forgets to enter the value after clearing it completely.
				if(updatedValue != 0)
					updatedValue = +updatedValue || 1;

				// Disable the minus button when the scale is 0.1 or below, and set scale to 0.1.
				if(updatedValue <= 0.1){
					updatedValue = 0.1;
					scaleRangeMinus.disabled = true;
				}
				// Disable the plus button when the scale is 100 or above, and set scale to 100.
				else if(updatedValue >= 100){
					updatedValue = 100;
					scaleRangePlus.disabled = true;
				}
				// Otherwise, enable both the plus as well as the minus buttons and set the scale to 1 decimal place.
				else{
					scaleRangeMinus.disabled = false;
					scaleRangePlus.disabled = false;
					updatedValue = updatedValue.toFixed(1);
				}

				// Update the value on both the input box as well as the range.
				scaleInput.value = updatedValue;
				scaleInputRange.value = updatedValue;
				scale = updatedValue;

				drawTheOutputLine();
			}

			function scaleMinusOne(){
				// Subtracts 1 from the value of scale.
				updateScale(+scale - 1);
			}

			function scalePlusOne(){
				// Adds 1 to the value of scale.
				updateScale(+scale + 1);
			}

			function updatePassingPointx(updatedValue){
				// Handle user's carelessness, when he/she forgets to enter the value after clearing it completely.
				// Using the unary plus for converting updatedValue to Number.
				if(updatedValue != 0)
					updatedValue = +updatedValue || 0;

				if(angle % 180 == 0){
					passingPoint[0] = updatedValue;
				}
				else if(angle % 90 == 0){
					passingPoint[0] = updatedValue;
					intercept = updatedValue;
				}
				else{
					passingPoint[0] = updatedValue;
					intercept = getIntercept();
					// console.log(intercept);
				}

				// Now update the values in their respective input boxes.
				passingPointx.value = passingPoint[0];
				passingPointy.value = passingPoint[1];
				interceptInput.value = intercept;

				drawTheOutputLine();
			}

			function updatePassingPointy(updatedValue){
				if(updatedValue != 0)
					updatedValue = +updatedValue || 0;

				if(angle % 180 == 0){
					passingPoint[1] = updatedValue;
					intercept = updatedValue;
				}
				else if(angle % 90 == 0){
					passingPoint[1] = updatedValue;
					intercept = passingPoint[0];
				}
				else{
					passingPoint[1] = updatedValue;
					intercept = getIntercept();
					// console.log(intercept);
				}

				// Now update the values in their respective input boxes.
				passingPointx.value = passingPoint[0];
				passingPointy.value = passingPoint[1];
				interceptInput.value = intercept;

				drawTheOutputLine();
			}
// By  Santanu Sikder
			function updateAngle(updatedValue){
				if(updatedValue != 0)
					updatedValue = +updatedValue || 45;

				// Update the value of angle.
				angle = updatedValue;

				// Update the slope and intercept using the respective getter functions and change the labels on the intercept increasing and decreasing buttons to up and down arrows respectively, if the line is not vertical.
				if(!(angle % 90 == 0 && angle % 180 != 0)){
					slope = getSlope(toRadians(angle));
					intercept = getIntercept();
					interceptMinus.innerHTML = "&darr;";
					interceptPlus.innerHTML = "&uarr;";
				}
				// But if the line is vertical, assign the x-coordinate of the passing point to the intercept and change the labels on the intercept increasing and decreasing buttons to left and right arrows respectively.
				else{
					intercept = passingPoint[0];
					interceptMinus.innerHTML = "&larr;";
					interceptPlus.innerHTML = "&rarr;";
				}

				// Update the values on the respective inputs;
				angleInput.value = angle;
				interceptInput.value = intercept;

				drawTheOutputLine();
			}

			function angleMinusOne(){
				// Subtracts 1 from the value of angle.
				updateAngle(+angle - 1);
			}

			function anglePlusOne(){
				// Adds 1 to the value of angle.
				updateAngle(+angle + 1);
			}

			function updateIntercept(updatedValue){
				updatedValue = +updatedValue || 0;

				// The amount of increase in the intercept after this action.
				var increaseInTheIntercept = updatedValue - intercept;

				// Update the value of the intercept.
				intercept = updatedValue;

				// Update the passing point
				if(angle % 90 == 0 && angle % 180 != 0){
					passingPoint[0] = intercept;
					passingPointx.value = intercept;
				}
				else{
					passingPoint[1] += increaseInTheIntercept;
					passingPointy.value = passingPoint[1];
				}

				// Update the value in the input;
				interceptInput.value = updatedValue;

				drawTheOutputLine();
			}

			function interceptMinusOne(){
				// Subtracts 1 from the value of intercept.
				updateIntercept(+intercept - 1);
			}

			function interceptPlusOne(){
				// Adds 1 to the value of intercept.
				updateIntercept(+intercept + 1);
				// console.log(window.orientation);
			}

			// Let me do some blah! blah! blah!!
			alert("Line Equation Finder v1.1\n\n* Use the easy to use GUI to find the equation of your desired line (Scale of the graph has a limited range: 0.1 - 100).\n* You can change the passing point, angle with the +ve x-axis (in anticlockwise sense), intercept or range.\n* Use the (0, 0) button to bring the origin back to the center of the box.\n* Check the box after CPP to ensure that the passing point is centered everytime any change is made.\n* It can be helpful in simple geometry or for quick use while regression analysis (just to get an idea).\n* There might be orientation-change based glitches in few devices.");

			drawTheOutputLine();
			// console.log(size);
			// console.log(canvasSize);
			// console.log(canvas.width);
		</script>
	</body>
</html>
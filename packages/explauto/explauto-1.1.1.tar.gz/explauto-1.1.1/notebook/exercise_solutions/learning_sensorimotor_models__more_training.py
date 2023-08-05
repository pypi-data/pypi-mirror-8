# Same as above, but first train the model with 10000 novel points:
for m in environment.random_motors(10000):
    s = environment.compute_sensori_effect(m)
    model.update(m, s)

ax = axes()

# Define the line and plot it:
x = 0.8
y_a = 0.5
y_b = -0.5
ax.plot([x, x], [y_a, y_b], color='red')

# for 10 points equidistantly spaced on the line, perform inverse prediction and plot:
for y in linspace(-0.5, 0.5, 10):
    m = model.inverse_prediction([x, y])
    environment.plot_arm(ax, m)

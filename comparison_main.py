from dance_tracker import  start
import matplotlib.pyplot as plt

x, y, z = start('dance_2.mp4')
x2, y2, z2 = start('dance_3.mp4')

# Taking out the first 50 samples
# NOTE: You can also do x[::5] to take values at steps of 5(to get the entire span faster), but make sure the final lengths of both lists match
a = x[:50]
b = x2[:50]
c = y[:50]
d = y2[:50]
e = z[:50]
f = z2[:50]
# Plotting
plt.plot(a) # plots line for a
plt.plot(b) # line for b in the same window
plt.legend(['video 1', 'video 2'], loc = 'upper right')
plt.title('Trends for the distance between feet for the two videos')
plt.xlabel('dist')
plt.ylabel('time')
plt.show()

plt.plot(c)
plt.plot(d)
plt.title('Trends for the distance between hands for the two videos')
plt.xlabel('dist')
plt.ylabel('time')
plt.show()

plt.plot(e)
plt.plot(f)
plt.title('Trends for the angle of the right hand')
plt.xlabel('angle')
plt.ylabel('time')
plt.show() # If you don't type this on pycharm, the plot wont appear

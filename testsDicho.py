import matplotlib.pyplot as plt
listeiteration=[0,1, 2, 3, 4, 5, 6, 7, 8, 9]
listePHI=[1.5, 1.75, 1.875, 1.9375, 1.96875, 1.984375, 1.9921875, 1.99609375, 1.998046875, 1.9990234375]
#fig=plt.figure(figsize=(6,6))
axs=plt.axes()
axs.axis([min(listeiteration)-0.2*min(listeiteration),max(listeiteration)+0.2*max(listeiteration),min(listePHI)-0.2*min(listePHI),max(listePHI)+0.2*max(listePHI)])
plt.scatter(listeiteration,listePHI, color = 'red')
plt.grid()
plt.plot(listeiteration,listePHI)

plt.title('Graph')
plt.xlabel('Itération')
plt.ylabel('Résultante des forces N')
plt.title("Résultante des forces au cours de la simulation")
plt.show()
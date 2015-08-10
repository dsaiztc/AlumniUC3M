ggplot(superior, aes(x = year_start, y = ..density..)) + 
  geom_histogram(binwidth = 1) + 
  facet_wrap(~duration)

ggplot(superior, aes(x = duration, y = ..density..)) + 
  geom_histogram(binwidth = 1) + 
  facet_wrap(~year_start)

teleco <- alumni[alumni$degree == 'Ingenieria Industrial', ]
ggplot(teleco, aes(x = duration, color = factor(year_start))) + 
  geom_freqpoly(binwidth = 1)

ggplot(grado, aes(x = duration, y = ..count.., fill = factor(year_start))) + 
  geom_density(binwidth = 1, alpha = .3, color = NA) +
  facet_wrap(~degree)
  
superior5 <- superior %>% filter(duration >= 5)
path_image <- paste(path_images, 'superior5.png', sep = '')
png(path_image, 800, 200)
p <- ggplot(superior5, aes(x = duration)) + 
  geom_histogram(binwidth = 1, origin = -0.5) +
  facet_wrap(~degree, ncol = 3) + 
  xlab('Tiempo en terminar la carrera (Años)') +
  ylab('Número de alumnos') +
  ggtitle('Ingeniería Superior')
p
dev.off()

teleco5 <- teleco[teleco$duration >= 5, ]
count(teleco5[teleco5$duration <= 6, ])/count(teleco5) * 100

summarise_and_save(superior5, path_doc)
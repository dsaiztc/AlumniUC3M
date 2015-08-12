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

###########################################################################
teleco <- alumni[alumni$degree == 'Ingenieria en Telecomunicacion', ]
teleco_start <- teleco %>% 
                  group_by(year_start) %>% 
                  summarize(mean = mean(duration), median = median(duration), sum = n())

ggplot(teleco_start, aes(x = year_start)) + 
  geom_line(aes(y = mean, color = 'blue')) +
  geom_line(aes(y = median, color = 'red'))

ggplot(superior, aes(x = year_start, y = duration, color=degree)) +
  geom_smooth()

ggplot(grado, aes(x = duration)) +
  geom_freqpoly(aes(color = degree), binwidth = 1, size = 1)

grado_teleco <- grado %>% 
                  filter(degree %in% c("Grado en Ingenieria de Sistemas Audiovisuales",
                                       "Grado en Ingenieria Telematica",
                                       "Grado en Ingenieria de Sistemas de Comunicaciones",
                                       "Grado en Ingenieria en Tecnologias de Telecomunicacion"))
ggplot(grado_teleco, aes(x = duration)) +
  geom_freqpoly(aes(color = degree, fill = degree), binwidth = 1, size = 1) +
  geom_area(aes(y = ..count.., fill = degree), stat = 'bin', binwidth = 1, alpha = 0.3) +
  geom_freqpoly(binwidth = 1) + 
  geom_area(aes(y = ..count..), stat = 'bin', binwidth = 1, alpha = 0.1)

ggplot(grado_teleco, aes(x = duration)) +
  geom_histogram(aes(y = ..density.., fill = degree), 
                 binwidth = 1, 
                 size = 1, 
                 alpha = 0.3, 
                 origin = -0.5, 
                 position = 'identity') +
  scale_x_continuous(limits = c(0, 8), breaks = seq(0, 8, 1))

# Superior students that needed more thatn 5 years
sum(superior$duration > 5)/length(superior$duration) * 100

# Teleco students that needed more thatn 5 years
sum(teleco$duration > 5)/length(teleco$duration) * 100

# Superior (>4) students that needed more thatn 5 years
superior5 <- superior[teleco$duration >= 5, ]
sum(superior5$duration > 5)/length(superior5$duration) * 100

# Teleco (>4) students that needed more thatn 5 years
teleco5 <- teleco[teleco$duration >= 5, ]
sum(teleco5$duration > 5)/length(teleco5$duration) * 100

# Duration 5 or more years, finishing from 2010 to 2014
teleco_my_cohort <- teleco %>% 
                      filter(duration > 4) %>% 
                      filter(year_fin %in% seq(2010, 2014, 1))
sum(teleco_my_cohort$duration <= 6)/length(teleco_my_cohort$duration)*100
cohort_mean <- mean(teleco_my_cohort$duration)
ggplot(teleco_my_cohort, aes(x = duration, y = ..density..)) + 
  scale_x_continuous(limits = c(4, 19), breaks = seq(4, 19, 1)) + 
  geom_histogram(binwidth = 1, origin = -0.5, alpha = 0.2) +
  geom_density(size = 1, color = '#808080') +
  geom_vline(aes(xintercept = cohort_mean), size = 1, color = '#808080', linetype = 'dashed') + 
  ggtitle('Time-to-finish distribution - Telecommunications Engineering - (grad years 2010 to 2014)') +
  xlab('Time (years)') +
  ylab('Density') +
  geom_text(aes(cohort_mean, 0.18, label = paste('mean = ', cohort_mean), hjust = -0.5), color = '#808080') +
  theme_grey()



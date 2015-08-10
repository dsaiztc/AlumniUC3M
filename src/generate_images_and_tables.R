library(ggplot2)
library(magrittr)
library(tidyr)
library(dplyr)
library(pander)

path_base_data <- '../data/'
path_data <- '2015-07-29'
path_alumni <- paste(path_base_data, path_data, '/', 'alumni_anonymous_clean.csv', sep = '')
path_base_doc <- '../doc/'

# Read cleaned alumni data
alumni <- read.csv(path_alumni, na.strings = c('-'), colClasses = c('character', 'character', 'numeric', 'numeric'))

# Create duration column (years)
alumni$duration <- alumni$year_fin - alumni$year_start

# Change 'tag' column name to 'specialization'
alumni$specialization <- alumni$tag
alumni$tag <- NULL

# Create data frames for different kind of grades
alumni_cp <- alumni
master <- alumni_cp %>% filter(grepl('Master', degree))
alumni_cp <- alumni_cp %>% filter(!grepl('Master', degree))
doctorado <- alumni_cp %>% filter(grepl('Doctorado', degree))
alumni_cp <- alumni_cp %>% filter(!grepl('Doctorado', degree))
grado <- alumni_cp %>% filter(grepl('Grado', degree))
alumni_cp <- alumni_cp %>% filter(!grepl('Grado', degree))
tecnica <- alumni_cp %>% filter(grepl('Tecnica', degree))
superior <- alumni_cp %>% filter(!grepl('Tecnica', degree))
rm(alumni_cp)

# Create Markdown tables summarizing data for different categories
summarise_and_save <- function(df_kind_degree, path_doc){
  alumni_cp <- df_kind_degree
  alumni_summary <- alumni_cp %>% 
                        group_by(degree) %>% 
                        summarise(mean = mean(duration), 
                                  median = median(duration), 
                                  sd = sd(duration), 
                                  num_alumni = n(),
                                  min_year_start = min(year_start),
                                  max_year_finish = max(year_fin)) %>% 
                        arrange(desc(median))
  write(pandoc.table.return(alumni_summary, style = "rmarkdown", split.tables = Inf), file = path_doc, append = TRUE)
}
summarise_and_save_with_specialization <- function(df_kind_degree, path_doc){
  alumni_cp <- df_kind_degree
  alumni_summary <- alumni_cp %>% 
                        group_by(degree, specialization) %>% 
                        summarise(mean = mean(duration), 
                                  median = median(duration), 
                                  sd = sd(duration), 
                                  num_alumni = n(),
                                  min_year_start = min(year_start),
                                  max_year_finish = max(year_fin)) %>% 
                        arrange(desc(median))
  write(pandoc.table.return(alumni_summary, style = "rmarkdown", split.tables = Inf), file = path_doc, append = TRUE)
}

path_doc <- paste(path_base_doc, 'tables.md', sep = '')
if (file.exists(path_doc)) file.remove(path_doc)
summarise_and_save(superior, path_doc)
summarise_and_save_with_specialization(tecnica, path_doc)
summarise_and_save(grado, path_doc)
summarise_and_save(master, path_doc)
summarise_and_save(doctorado, path_doc)

# Visualizations for the different groups
path_images <- paste(path_base_doc, 'images/', sep = '') 

path_image <- paste(path_images, 'grado.png', sep = '')
png(path_image, 800, 600)
p <- ggplot(grado, aes(x = duration)) + 
  geom_histogram(binwidth = 1, origin = -0.5) +
  facet_wrap(~degree, ncol = 3) + 
  scale_x_continuous(limits = c(0, max(grado$duration)), breaks = seq(0, max(grado$duration), 1)) +
  xlab('Tiempo en terminar la carrera (Años)') +
  ylab('Número de alumnos') +
  ggtitle('Grados')
print(p)
dev.off()

path_image <- paste(path_images, 'superior.png', sep = '')
png(path_image, 800, 200)
p <- ggplot(superior, aes(x = duration)) + 
  geom_histogram(binwidth = 1, origin = -0.5) +
  facet_wrap(~degree, ncol = 3) + 
  scale_x_continuous(limits = c(0, max(superior$duration)), breaks = seq(0, max(superior$duration), 1)) +
  xlab('Tiempo en terminar la carrera (Años)') +
  ylab('Número de alumnos') +
  ggtitle('Ingeniería Superior')
print(p)
dev.off()

path_image <- paste(path_images, 'master.png', sep = '')
png(path_image, 800, 600)
p <- ggplot(master, aes(x = duration)) + 
  geom_histogram(binwidth = 1, origin = -0.5) +
  facet_wrap(~degree, ncol = 3) + 
  scale_x_continuous(limits = c(0, max(master$duration)), breaks = seq(0, max(master$duration), 1)) +
  xlab('Tiempo en terminar la carrera (Años)') +
  ylab('Número de alumnos') +
  ggtitle('Máster')
print(p)
dev.off()

path_image <- paste(path_images, 'tecnica.png', sep = '')
png(path_image, 800, 200)
p <- ggplot(tecnica, aes(x = duration)) + 
  geom_histogram(binwidth = 1, origin = -0.5) +
  facet_wrap(~degree, ncol = 3) + 
  scale_x_continuous(limits = c(0, max(tecnica$duration)), breaks = seq(0, max(tecnica$duration), 1)) +
  xlab('Tiempo en terminar la carrera (Años)') +
  ylab('Número de alumnos') +
  ggtitle('Ingeniería Técnica')
print(p)
dev.off()
data <- read.csv("cs_data/percent_contributions.csv")
head(data)

columns <- c("percent_O3S1OCT", "percent_O1S0OCT", "percent_O3P0OCT", "percent_O3S1SING")

results <- list()

for (col in columns) {
  threshold <- quantile(data[[col]], 0.99)
  large_values <- data[data[[col]] > threshold, ]

  subdomain_x <- range(large_values$x, na.rm=TRUE)
  subdomain_z <- range(large_values$z, na.rm=TRUE)
  subdomain_Q <- range(large_values$Q, na.rm=TRUE)
  subdomain_PT <- range(large_values$PT, na.rm=TRUE)

  results[[col]] <- list(
      x_range = subdomain_x,
      z_range = subdomain_z,
      Q_range = subdomain_Q,
      PT_range = subdomain_PT
  )
  
  print(col)
  print(results[[col]])
}
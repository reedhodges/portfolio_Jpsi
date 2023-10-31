data <- read.csv("cs_data/percent_contributions.csv")
head(data)
threshold <- quantile(data$percent_O3S1OCT, 0.99)
large_values <- data[data$percent_O3S1OCT > threshold, ]
subdomain_x <- range(large_values$x)
subdomain_z <- range(large_values$z)
subdomain_Q <- range(large_values$Q)
subdomain_PT <- range(large_values$PT)

print(subdomain_x)
print(subdomain_z)
print(subdomain_Q)
print(subdomain_PT)
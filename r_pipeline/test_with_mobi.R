# r_pipeline/test_with_mobi.R
library(seminr)
data(mobi)
write.csv(mobi, "/tmp/mobi_test.csv", row.names = FALSE)
cat("mobi dataset written to /tmp/mobi_test.csv\n")
cat("Columns:", paste(colnames(mobi), collapse = ", "), "\n")
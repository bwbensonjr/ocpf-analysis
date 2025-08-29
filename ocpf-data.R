library(tidyverse)
library(janitor)

legislative_offices <- c(
    "House",
    "Senate",
    "Governor's Council"    
)

convert_date_columns <- function(df, format="%m/%d/%Y") {
    df |>
        mutate(across(contains("Date", ignore.case=FALSE),
                      ~as.Date(.x, format=format)))
}

districts <-
    read_tsv("data/districts/district_code_list.txt") |>
    clean_names() |>
    filter(office_type_description %in% legislative_offices)

filers <-
    read_tsv("data/filers/candidates.txt") |>
    convert_date_columns() |>
    clean_names() |>
    filter(
        (office_type_sought %in% legislative_offices),
        is.na(closed_date)
    ) |>
    mutate(is_incumbent = (district_code_sought = district_code_held))

reports <- read_tsv("data/reports/reports.txt") |>
    convert_date_columns() |>
    clean_names()

report_items <- read_tsv("data/reports/report-items.txt") |>
    convert_date_columns() |>
    clean_names()

account_types <-
    read_tsv("data/account-types/Account_Types.txt") |>
    clean_names()

filers_reports <- filers |>
    nest_join(reports, by="cpf_id") |>
    mutate(num_reports = map_int(reports, nrow))

filers_reports |>
    filter(office_type_sought == "House",
           district_name_sought == "14th Bristol") |>
    select(
        cpf_id,
        candidate_first_name,
        candidate_last_name,
        party_affiliation,
        organization_date,
        closed_date,
        district_name_held,
        num_reports
    )


recent_filers <- filers |>
    filter(organization_date >= "2025-08-01") |>
    arrange(desc(organization_date))

recent_filers |>
    select (
        organization_date,
        account_type_code,
        district_name_sought,
        cpf_id,
        candidate_first_name,
        candidate_last_name,
    )

filers_inc <- filers |>
    filter(office_type_held %in% c("House", "Senate", "Governor's Council"))

filers_reports <- filers |>
    nest_join(reports, by="cpf_id") |>
    mutate(num_reports = map_int(reports, nrow))

filers_reports |>
    filter(office_type_sought == "House",
           district_name_sought == "14th Bristol") |>
    select(
        cpf_id,
        candidate_first_name,
        candidate_last_name,
        party_affiliation,
        organization_date,
        closed_date,
        district_name_held,
        num_reports
    )

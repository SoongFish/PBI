library(gapminder)

gapminder[gapminder$country == "Korea, Rep." & gapminder$year >= 1990, c("country", "year", "lifeExp", "pop")]

gapminder[gapminder$country == "Korea, Dem. Rep." & gapminder$year >= 1990, c("country", "year", "lifeExp", "pop")]
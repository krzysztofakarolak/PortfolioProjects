select * 
from PortfolioProject.dbo.CovidDeaths
order by 3,4

-- select data that we are going to be using

select location, date,total_cases, new_cases, total_deaths, population
from PortfolioProject..CovidDeaths
order by 1,2

-- looking at total cases and total deaths -- DeathPerc.
-- shows likelihood od dying if you contract covid in your country
select location,date,total_cases,total_deaths,(total_deaths/total_cases)*100 as DeathPercaentage
from PortfolioProject..CovidDeaths
where location like '%states%' -- your country
order by 1,2

--looking at total cases vs. population
-- shows what percentage of the population got covid
select location,date,total_cases, population,(total_cases/population)*100 as PopPerc
from PortfolioProject..CovidDeaths
where location like '%states%'
order by 1,2

-- looking at countries with the highest infection rate compared to the population
select location, population, max(total_cases) as InfRate, max((total_cases/population))*100 as PopPercInf
from PortfolioProject..CovidDeaths
group by location, population
order by 4 desc

--showing countries with the highest death count for population
select location, max(cast(total_deaths as int)) as TotDeathsCount
from PortfolioProject..CovidDeaths
where continent is not null
group by location
order by 2 desc

-- let's break things down by contitnent
select location, max(cast(total_deaths as int)) as TotDeathsCount
from PortfolioProject..CovidDeaths
where continent is null
group by location
order by 2 desc

-- that way would be wrong
select continent, max(cast(total_deaths as int)) as TotDeathsCount
from PortfolioProject..CovidDeaths
where continent is not null
group by continent
order by 2 desc

--calculate everything across the entire world
-- GLOBAL NUMBERS
select  sum(new_cases) as totalCases, sum(cast(new_deaths as int)) as TotalDeaths, (sum(cast(new_deaths as int))/sum(new_cases))*100 as DeathPerc
from PortfolioProject..CovidDeaths
where continent is not null
-- group by date
order by 1,2


--total population vs vaccinations
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.location, dea.date) as rolling_vac
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
order by 2,3


-- use cte
with PopvsVac (Continent, location, date, population, new_vaccinations, rolling_vac)
as (
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_vac
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
--order by 2,3
)
select * , (rolling_vac/population)*100
from PopvsVac

-- temp table
drop table if exists  #PercentPopulationVaccinated
create table #PercentPopulationVaccinated (Continent nvarchar(255), 
location nvarchar(255), date datetime, population numeric, new_vaccinations numeric, rolling_vac numeric)
insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_vac
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location=vac.location and dea.date=vac.date
--where dea.continent is not null
--order by 2,3

select *, (rolling_vac/population)*100
from #PercentPopulationVaccinated

--creating a view to store data for later visualizations
create view PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_vac
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
--order by 2,3

select *
from PercentPopulationVaccinated


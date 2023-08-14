/* CLEANING DATA IN SQL QUERIES */
-- Most of the code below shows rather a work progression than a final code


select *
from PortfolioProject.dbo.NashvilleHousing

--- Standardize data format ---
select SaleDate, convert(date, SaleDate)
from PortfolioProject.dbo.NashvilleHousing
---------------------------------------------------------- Sometimes it would be enough to just add:
select SaleDateConverted, convert(date, SaleDate)       --   update PortfolioProject.dbo.NashvilleHousing
from PortfolioProject.dbo.NashvilleHousing              --   set SaleDate=convert(date,SaleDate)
alter table PortfolioProject.dbo.NashvilleHousing       
add SaleDateConverted Date;                             

update PortfolioProject.dbo.NashvilleHousing
set SaleDateConverted=convert(date,SaleDate)

--- Populate Property Address data ---
select *
from PortfolioProject.dbo.NashvilleHousing
--where PropertyAddress is null							-- <-- checking which properties don't have filled address
order by ParcelID										-- <-- after swithching off where statement, we're checking if parcel ids have sth in common, they do
														--     we can populate PropertyAddress column as parcels that have the same ids have the same address

select a.ParcelID, a.PropertyAddress,					-- <-- we're looking for properties, which PropertyAddress is empty (NULL)
b.ParcelID, b.PropertyAddress
from PortfolioProject.dbo.NashvilleHousing	a
join PortfolioProject.dbo.NashvilleHousing  b
	on a.ParcelID=b.ParcelID 
	and a.[UniqueID ]<>b.[UniqueID ]
where a.PropertyAddress is null


select a.ParcelID, a.PropertyAddress,					
b.ParcelID, b.PropertyAddress ,
isnull(a.PropertyAddress, b.PropertyAddress)			-- <-- we're preparting a column, which will later fill a.PropertyAddress with b.PropertyAddress
from PortfolioProject.dbo.NashvilleHousing	a			--		in the command isnull(x,y) we can insert in y some strings too (e.g. 'abcde')
join PortfolioProject.dbo.NashvilleHousing  b
	on a.ParcelID=b.ParcelID 
	and a.[UniqueID ]<>b.[UniqueID ]
where a.PropertyAddress is null

update a
set PropertyAddress=isnull(a.PropertyAddress, b.PropertyAddress)	-- <-- filling column with data, after running/executing this code, then the one above
from PortfolioProject.dbo.NashvilleHousing	a						--		will return empty table (only headings)
join PortfolioProject.dbo.NashvilleHousing  b
	on a.ParcelID=b.ParcelID 
	and a.[UniqueID ]<>b.[UniqueID ]
where a.PropertyAddress is null


--- Breaking out Address into Individual Columns (Address, City, State) ---
																		  
select PropertyAddress
from PortfolioProject.dbo.NashvilleHousing
																		  -- let's show, what data our new columns will have
select																	  -- CHARINDEX(x,y) statement takes data in y, searches for x, and returns int (number in which x stands)
substring(PropertyAddress, 1, charindex(',',PropertyAddress)-1) as Address,		-- we have to take one sing out, as it is comma, that why there is -1
substring(PropertyAddress, charindex(',',PropertyAddress)+1, len(PropertyAddress)) as City		-- similar to above, but +1; LEN(x) returns the lenght of x string (int)
from PortfolioProject.dbo.NashvilleHousing

alter table PortfolioProject.dbo.NashvilleHousing						  -- <-- we're adding new column
add PropertySplitAddress nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing							  -- <-- we're filling the column with data
set PropertySplitAddress=substring(PropertyAddress, 1, charindex(',',PropertyAddress)-1)

alter table PortfolioProject.dbo.NashvilleHousing
add PropertyCity nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set PropertyCity=substring(PropertyAddress, charindex(',',PropertyAddress)+1, len(PropertyAddress))

select *																  -- here we can see that those two new columns are added and filled, they're at the end of the table
from PortfolioProject.dbo.NashvilleHousing

select OwnerAddress														  -- showing what we will part next
from PortfolioProject.dbo.NashvilleHousing

select OwnerAddress,													  -- parting OwnerAddress column in to three different: Address, City, and State
parsename(replace(OwnerAddress,',','.'),3),								  -- statement PARSENAME(x,y) takes string and extract from it a string beginning from the end of the given string
parsename(replace(OwnerAddress,',','.'),2),								  -- to the y (this needs to be number) dot given in x, or to the beginning of the given string.
parsename(replace(OwnerAddress,',','.'),1)								  -- that' why we had to replace commas with dot in OwnerAddress.
from PortfolioProject.dbo.NashvilleHousing

-- let's add those columns to table

alter table PortfolioProject.dbo.NashvilleHousing
add OwnerSplitAddress nvarchar(255), OwnerSplitCity nvarchar(255), OwnerSplitState nvarchar(255);

-- let's fill them up

update PortfolioProject.dbo.NashvilleHousing
set OwnerSplitAddress=parsename(replace(OwnerAddress,',','.'),3),
OwnerSplitCity=parsename(replace(OwnerAddress,',','.'),2),
OwnerSplitState=parsename(replace(OwnerAddress,',','.'),1)

select *																  -- again, here we can see that those two new columns are added and filled, 
from PortfolioProject.dbo.NashvilleHousing								  -- they're at the end of the table, preferably delete this kind of code after checking
--where OwnerAddress is not null


--- Change Y and N to Yes and No in "Sold as Vacant" field ---

select distinct(SoldAsVacant), count(SoldAsVacant)						  -- showing what data might be in columnt (distinct statement), how many times is it used
from PortfolioProject.dbo.NashvilleHousing
group by SoldAsVacant
order by 2																  -- let' check which way is more popular

select SoldAsVacant,
	case when SoldAsVacant='Y' then 'Yes'								  -- creating column with more popular signature for items with the less popular ones
		 when SoldAsVacant='N' then 'No'
		 else SoldAsVacant 
	end
from PortfolioProject.dbo.NashvilleHousing
--where SoldAsVacant='Y' or SoldAsVacant='N'							  -- checking if it works

update PortfolioProject.dbo.NashvilleHousing
set SoldAsVacant=
	case when SoldAsVacant='Y' then 'Yes'					  -- changing less pop sign. to more pop one
		 when SoldAsVacant='N' then 'No'
		 else SoldAsVacant 
	end

--- Remove Duplicates ---
with RowNumCTE as(										-- needs to be run everytime it's used
select *,												-- here we're showing that some properties have more than one unique id, when a property has the 2nd uid than the row_num is 2 etc.
	ROW_NUMBER() over (
	partition by	ParcelID,
					PropertyAddress,
					SalePrice,
					SaleDate,
					LegalReference 
					order by 
						UniqueID
						) row_num
from PortfolioProject.dbo.NashvilleHousing
--order by ParcelID
)

select *																-- showing duplicates, after running DELETE statement below, returns empty table
from RowNumCTE
where row_num>1
order by PropertyAddress

delete																	-- deleting duplicates
from RowNumCTE
where row_num>1


--- Delete unused columns ---

select * 
from PortfolioProject.dbo.NashvilleHousing

alter table PortfolioProject.dbo.NashvilleHousing						-- deleting columns in raw data, use carefully
drop column OwnerAddress, TaxDistrict, PropertyAddress, SaleDate
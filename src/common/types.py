from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

# ID TYPES

type AirplaneId = int
type BookingId = UUID
type CurrentStatusId = int
type DocumentId = UUID
type FlightId = UUID
type PassengerId = UUID
type RouteId = int
type TicketId = UUID

# COMMON TYPES

type PaidAmountUsd = Decimal
type IssueCountry = str

# BOOKING TYPES

type BookingReference = str
type BookingDatetime = datetime
type BookingRow = tuple[BookingId, BookingReference, BookingDatetime, PaidAmountUsd, CurrentStatusId]

# DOCUMENT TYPES

type DocumentNumber = str
type ValidFrom = date
type ValidUntil = date
type DocumentTypeId = int
type DocumentRow = tuple[DocumentId, DocumentNumber, ValidFrom, ValidUntil, IssueCountry, PassengerId, DocumentTypeId]
type DocumentIdentityKey = tuple[DocumentNumber, IssueCountry]

# FLIGHT TYPES

type ScheduledDepartureDatetime = datetime
type ScheduledArrivalDatetime = datetime
type ActualDepartureDatetime = datetime | None
type ActualArrivalDatetime = datetime | None
type OperatingCostUsd = Decimal
type BasePriceUsd = Decimal
type FlightRow = tuple[FlightId, ScheduledDepartureDatetime,  ScheduledArrivalDatetime,  ActualDepartureDatetime,  ActualArrivalDatetime,  OperatingCostUsd, BasePriceUsd, CurrentStatusId, RouteId, AirplaneId]
type FlightIdentityKey = tuple[ScheduledDepartureDatetime, RouteId]

# PASSENGER TYPES

type NationalIdentityNumber = str
type FullName = str
type BirthDate = date
type Email = str
type PhoneNumber = str
type IsBlacklisted = bool
type IsVip = bool
type PassengerRow = tuple[PassengerId, NationalIdentityNumber, IssueCountry, FullName, BirthDate, Email, PhoneNumber, IsBlacklisted, IsVip]
type PassengerIdentityKey = tuple[NationalIdentityNumber, IssueCountry]

# TICKET TYPES

type TicketNumber = str
type TicketRow = tuple[TicketId, TicketNumber, PaidAmountUsd, CurrentStatusId, BookingId, FlightId, PassengerId]

# ROUTE TYPES

type FlightNumber = str
type Origin = str
type Destination = str
type DistanceKm = int
type DurationMin = int
type RouteRow = tuple[RouteId, FlightNumber, Origin, Destination, DistanceKm, DurationMin]
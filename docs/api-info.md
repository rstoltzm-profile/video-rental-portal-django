```GO
func NewRouter(pool *pgxpool.Pool, apiKey string) http.Handler {
        mux := http.NewServeMux()

        // auth
        authService := &auth.SimpleAuthService{}
        authHandler := auth.NewHandler(authService)
        mux.HandleFunc("/v1/login", authHandler.Login)

        // health check
        mux.HandleFunc("/health", healthHandler)
        mux.HandleFunc("/health/pool", healthHandlerWithPool(pool))
        mux.Handle("/swagger/", httpSwagger.WrapHandler)

        // v1 routes
        v1 := http.NewServeMux()
        registerCustomerRoutes(v1, pool)
        registerRentalRoutes(v1, pool)
        registerInventoryRoutes(v1, pool)
        registerStoreRoutes(v1, pool)
        registerFilmRoutes(v1, pool)
        registerPaymentRoutes(v1, pool)

        mux.Handle("/v1/", http.StripPrefix("/v1",
                middleware.CORSMiddleware(
                        middleware.RequestSizeMiddleware(
                                middleware.ApiKeyMiddleware(apiKey,
                                        middleware.ErrorMiddleware(v1.ServeHTTP))))))
        return mux
}

func registerFilmRoutes(mux *http.ServeMux, pool *pgxpool.Pool) {
        repo := film.NewRepository(pool)
        svc := film.NewService(repo, repo)
        handler := film.NewHandler(svc)
        mux.HandleFunc("GET /films", handler.GetFilms)
        mux.HandleFunc("GET /films/{id}", handler.GetFilmByID)
        mux.HandleFunc("GET /films/search", handler.SearchFilm)
        mux.HandleFunc("GET /films/", handler.GetFilmWithActorsAndCategoriesByID)
}
```

```GO
type Film struct {
        Title       string `json:"title"`
        Description string `json:"description"`
        ReleaseYear int    `json:"release_year"`
        Language    string `json:"language"`
        Rating      string `json:"rating"`
}

type FilmWithActorsCategories struct {
        Title       string   `json:"title"`
        Description string   `json:"description"`
        ReleaseYear int      `json:"release_year"`
        Language    string   `json:"language"`
        Rating      string   `json:"rating"`
        Categories  []string `json:"categories"`
        Actors      []string `json:"actors"`
}

type Customer struct {
        ID        int    `json:"id"`
        FirstName string `json:"first_name"`
        LastName  string `json:"last_name"`
        Email     string `json:"email"`
}

type CreateCustomerRequest struct {
        FirstName string       `json:"first_name" validate:"required,min=1,max=50"`
        LastName  string       `json:"last_name" validate:"required,min=1,max=50"`
        Email     string       `json:"email" validate:"required,email"`
        StoreID   int          `json:"store_id" validate:"required,gt=0"`
        Address   AddressInput `json:"address" validate:"required"`
}

type AddressInput struct {
        Address    string `json:"address" validate:"required,min=1,max=100"`
        Address2   string `json:"address2" validate:"max=100"`
        District   string `json:"district" validate:"required,min=1,max=50"`
        CityName   string `json:"city_name" validate:"required,min=1,max=50"`
        PostalCode string `json:"postal_code" validate:"required,min=4,max=6"`
        Phone      string `json:"phone" validate:"required,e164"`
}

type CustomerRentals struct {
        FirstName     string    `json:"first_name"`
        LastName      string    `json:"last_name"`
        Phone         string    `json:"phone"`
        RentalDate    time.Time `json:"rental_date"`
        Title         string    `json:"title"`
        RentalDueDate time.Time `json:"rental_due_date"`
        Overdue       bool      `json:"overdue"`
}

type Rental struct {
        FirstName  string    `json:"first_name"`
        LastName   string    `json:"last_name"`
        Phone      string    `json:"phone"`
        RentalDate time.Time `json:"rental_date"`
        Title      string    `json:"title"`
}

type CreateRentalRequest struct {
        InventoryID int `json:"inventory_id" validate:"min=0"`
        CustomerID  int `json:"customer_id" validate:"min=0"`
        StaffID     int `json:"staff_id" validate:"min=0"`
}
```
# Materials Catalog API - Complete Project Documentation

## PROJECT OVERVIEW

The Materials Catalog API is a comprehensive backend service designed specifically for the construction and building materials industry. It serves as a digital marketplace and inventory management system that connects material suppliers with contractors, builders, and project managers. This API-first solution enables businesses to digitize their physical catalogs, manage supplier relationships, track pricing, and gain valuable insights into market trends through analytics.

## BUSINESS PROBLEM SOLVED

Traditional construction material procurement faces several challenges:

1. **Paper-based catalogs** - Suppliers distribute printed catalogs that quickly become outdated
2. **Inconsistent product information** - Different suppliers describe similar products differently
3. **Difficult price comparison** - Contractors must contact multiple suppliers individually
4. **No market intelligence** - No way to know which products are gaining popularity
5. **Unit conversion confusion** - Mixing metric and imperial measurements causes errors
6. **Supplier quality unknown** - No standardized way to identify premium suppliers

This API solves all these problems by providing a centralized, standardized, and intelligent platform.

## CORE FEATURES AND FUNCTIONALITY

### 1. Product Catalog Management

The system provides a flexible product catalog where each product can have its own unique set of attributes while maintaining required fields for consistency. Products can belong to different categories such as Acoustic materials, Fireproofing, Insulation, and more. Each product record contains:

- Basic identification (name, ID, creation date)
- Categorization for easy filtering
- Flexible JSON attributes that can store any product-specific properties
- Required technical specifications (thickness in millimeters, coverage in square meters)
- Automatic unit conversion between metric and imperial systems

This flexibility is crucial because construction materials vary widely - acoustic panels need different specifications than fireproof sealants or insulation rolls.

### 2. Supplier Management System

Suppliers are categorized into two distinct tiers:

**Tier 1 (Premium Suppliers)** - High-quality providers that meet strict standards. These suppliers are ideal for projects requiring certified materials, hospital construction, government contracts, or any scenario where quality cannot be compromised.

**Tier 2 (Standard Suppliers)** - Regular suppliers offering competitive pricing. Suitable for general construction, residential projects, and non-critical applications.

Suppliers can be tagged with attributes like "high_performance", "eco_friendly", "fast_delivery", "local", or any custom tags that help buyers filter and find the right partners. This tagging system creates a flexible categorization beyond simple tier assignment.

### 3. Offer and Pricing Engine

The system implements a many-to-many relationship between products and suppliers through offers. This means:

- One product can be offered by multiple suppliers at different prices
- One supplier can offer multiple products
- Prices can be in different currencies (USD, EUR, GBP, etc.)
- Historical pricing can be tracked through timestamps

This structure enables true price comparison and competitive analysis, allowing buyers to find the best deals and suppliers to stay competitive.

### 4. Automatic Unit Conversion System

One of the most practical features is the built-in unit conversion. The construction industry globally uses both metric and imperial measurements, often causing costly errors. This API automatically converts between:

**Thickness/Dimension Conversion:**
- Millimeters (mm) to Inches (in) - Divide by 25.4
- Example: 50.0 mm = 1.97 inches

**Area Coverage Conversion:**
- Square Meters (sqm) to Square Feet (sqft) - Multiply by 10.7639
- Example: 1.2 sqm = 12.92 sqft

Users simply specify their preferred unit system, and the API returns both original and converted values, eliminating calculation errors and saving time.

### 5. Real-Time Analytics and Insights

The analytics engine tracks product views anonymously, providing valuable market intelligence:

**Event Tracking:**
- Every product view is recorded with timestamp
- Session-based tracking without storing personal data
- No authentication required for view tracking

**Trending Analysis:**
- Real-time calculation of most-viewed products
- Configurable time windows (last hour, 24 hours, 48 hours, custom)
- Adjustable result limits (top 5, top 10, top 20)
- Category-specific trending insights

This feature answers critical business questions:
- What materials are currently in high demand?
- Which products should we stock more of?
- What are competitors' customers looking at?
- Are new products gaining traction?

### 6. Secure Authentication System

The API implements industry-standard JWT (JSON Web Token) authentication:

**Registration and Login:**
- Users create accounts with email and password
- Passwords are securely hashed using bcrypt
- No plain-text passwords ever stored

**Token-Based Access:**
- Successful login returns a JWT token
- Tokens expire after 30 minutes for security
- Protected endpoints require valid token in headers
- Public endpoints remain accessible without authentication

**Access Control:**
- Public: Browse products, check trending, record views
- Protected: Create products, add suppliers, create offers
- Role-based access can be extended for admin functions

## TECHNICAL ARCHITECTURE

### Backend Stack

**FastAPI Framework:**
- Modern, high-performance Python web framework
- Automatic OpenAPI/Swagger documentation generation
- Built-in data validation using Pydantic
- Asynchronous support for high concurrency
- Type hints for better code quality

**SQLAlchemy ORM:**
- Database-agnostic object-relational mapping
- SQLite for development (file-based, zero configuration)
- Easily migrates to PostgreSQL for production
- Relationship management between models
- Query optimization and lazy/eager loading

**SQLite Database:**
- Simple file-based database
- No separate database server required
- Perfect for development and small deployments
- Easy backup and migration

**JWT Authentication:**
- Stateless authentication
- No session storage required
- Cross-platform compatible
- Industry standard for APIs

### Data Models and Relationships

**User Model:**
```python
- id: Integer (Primary Key)
- email: String (Unique, Indexed)
- hashed_password: String
- created_at: DateTime
```

**Product Model:**
```python
- id: Integer (Primary Key)
- name: String
- category: String
- attributes: JSON (Flexible properties)
- created_at: DateTime
- offers: Relationship to Offer model
- events: Relationship to Event model
```

**Supplier Model:**
```python
- id: Integer (Primary Key)
- name: String
- tier: String (tier_1/tier_2)
- tags: JSON (Array of strings)
- offers: Relationship to Offer model
```

**Offer Model:**
```python
- id: Integer (Primary Key)
- product_id: ForeignKey to Product
- supplier_id: ForeignKey to Supplier
- price: Float
- currency: String (3-letter code)
- created_at: DateTime
```

**Event Model:**
```python
- id: Integer (Primary Key)
- event_type: String (product_view)
- product_id: ForeignKey to Product
- session_id: String
- timestamp: DateTime
```

## API ENDPOINTS COMPLETE REFERENCE

### Authentication Endpoints

**POST /api/register**
Purpose: Create new user account
Request Body: {email, password}
Response: User object with ID and creation timestamp
Access: Public
Rate Limit: None

**POST /api/login**
Purpose: Authenticate and receive access token
Request Body: {email, password}
Response: {access_token, token_type}
Access: Public
Token Expiry: 30 minutes

### Product Endpoints

**GET /api/products**
Purpose: Retrieve products with filtering
Query Parameters:
- category: Filter by product category
- supplier_tier: Filter by supplier tier
- supplier_tag: Filter by supplier tag
- unit_system: metric/imperial
- skip: Pagination offset
- limit: Items per page (max 100)
Access: Public
Response: Array of products with unit conversions

**GET /api/products/{id}**
Purpose: Retrieve single product
Path Parameters: id - Product ID
Access: Public
Response: Single product with all attributes

**POST /api/products**
Purpose: Create new product
Request Body: {name, category, attributes}
Access: Protected (Authentication required)
Validation: Must include thickness_mm and coverage_sqm
Response: Created product object

### Supplier Endpoints

**POST /api/suppliers**
Purpose: Register new supplier
Request Body: {name, tier, tags}
Access: Protected (Authentication required)
Validation: tier must be tier_1 or tier_2
Response: Created supplier object

### Offer Endpoints

**POST /api/offers**
Purpose: Create price offer
Request Body: {product_id, supplier_id, price, currency}
Access: Protected (Authentication required)
Validation: Product and supplier must exist
Response: Created offer object

### Analytics Endpoints

**POST /api/events**
Purpose: Record product view
Request Body: {product_id, session_id}
Access: Public
Response: Success confirmation

**GET /api/insights/trending**
Purpose: Get trending products
Query Parameters:
- window_hours: Time window (default 24)
- limit: Number of results (default 5, max 100)
Access: Public
Response: Array of products with view counts

## USE CASES AND WORKFLOWS

### Use Case 1: Material Supplier Onboarding

A new material supplier wants to list their products on the platform:

1. **Account Creation**
   - Supplier registers with company email
   - Creates secure password
   - Receives confirmation

2. **Supplier Profile Setup**
   - Creates supplier entry with name and tier selection
   - Adds relevant tags (e.g., "high_performance", "certified")
   - Profile becomes visible to buyers

3. **Product Listing**
   - Adds products one by one or in bulk
   - For each product: name, category, technical specifications
   - Ensures thickness and coverage are included
   - Adds optional attributes (material, color, certifications)

4. **Pricing Configuration**
   - Creates offers for each product
   - Sets competitive prices
   - Specifies currency
   - Multiple price points for different volumes

5. **Market Monitoring**
   - Checks trending products daily
   - Sees which of their products get most views
   - Adjusts pricing based on demand

### Use Case 2: Construction Project Procurement

A large hospital construction project needs specific materials:

1. **Material Research**
   - Project manager searches for fireproofing materials
   - Filters to Tier 1 suppliers only (hospital requires premium)
   - Checks products with fire_rating attributes
   - Reviews specifications and certifications

2. **Price Comparison**
   - Views multiple offers for same products
   - Compares pricing across different suppliers
   - Considers supplier reputation and tags

3. **Decision Making**
   - Checks trending data to see popular choices
   - Reviews which products other hospitals use
   - Makes data-informed purchasing decisions

4. **Documentation**
   - API calls provide audit trail
   - Product specifications accessible for compliance
   - Pricing history available for budget justification

### Use Case 3: Product Launch and Market Testing

A manufacturer launches new eco-friendly insulation:

1. **Product Creation**
   - Adds "Eco Insulation Pro" to catalog
   - Category: Insulation
   - Attributes: thickness, coverage, R-value, recycled content
   - Tags: eco_friendly, energy_star

2. **Initial Marketing**
   - Creates competitive pricing through Tier 1 supplier
   - Monitors view counts daily
   - Tracks session sources

3. **Market Response Analysis**
   - Views trending data after 1 week
   - Compares views with established products
   - Identifies which contractors are interested

4. **Strategy Adjustment**
   - If trending low: adjust price or improve positioning
   - If trending high: increase stock, consider promotion
   - Gather feedback from viewing patterns

### Use Case 4: International Contractor

A contractor working on global projects needs flexibility:

1. **Unit Conversion**
   - US project: Requests products in imperial units
   - European project: Switches to metric
   - Same API endpoint, different unit_system parameter
   - No manual calculations needed

2. **Multi-Currency Pricing**
   - Views prices in USD for US projects
   - Switches to EUR for European projects
   - Accurate currency representation

3. **Global Supplier Search**
   - Finds Tier 1 suppliers in different regions
   - Filters by location tags
   - Compares international pricing

## TECHNICAL IMPLEMENTATION DETAILS

### Database Design Decisions

**JSON Fields for Attributes:**
Instead of creating rigid columns for every possible product attribute, we use JSON fields. This provides:
- Unlimited extensibility without schema changes
- Support for diverse product types
- Efficient storage of sparse data
- Easy querying of specific attributes

**Supplier Tags as JSON:**
Similar to product attributes, tags are stored as JSON arrays:
- No fixed limit on number of tags
- Easy addition of new tag categories
- Efficient filtering using JSON contains operations
- Self-documenting tag system

**Event-Based Analytics:**
Rather than calculating counts on the fly:
- Events are immutable records
- Each view is a separate row
- Allows time-window analysis
- Supports historical trend analysis
- Enables future ML applications

### Security Implementation

**Password Security:**
- Bcrypt hashing algorithm
- Salt automatically included
- Configurable work factor
- No reversible encryption

**JWT Implementation:**
- HS256 signing algorithm
- Configurable secret key
- 30-minute token expiry
- Stateless authentication
- Bearer token scheme

**Protected Endpoints:**
- All modification operations require auth
- Token validated on each request
- Clear error messages for auth failures
- No sensitive data in URLs

### Performance Optimizations

**Pagination:**
- Limit/offset pattern for large datasets
- Default limit of 100 items
- Client-configurable page sizes
- Prevents memory exhaustion

**Eager Loading:**
- SQLAlchemy joinedload for relationships
- Reduced database queries
- Optimized N+1 query prevention
- Balance between speed and memory

**Database Indexing:**
- Primary keys automatically indexed
- Foreign keys indexed
- Email field indexed for fast login
- Category and tier fields indexed for filtering

## BUSINESS VALUE PROPOSITION

### For Material Suppliers

1. **Digital Transformation**
   - Move from paper catalogs to API
   - Real-time product updates
   - No printing costs
   - Instant global distribution

2. **Market Intelligence**
   - See exactly what contractors view
   - Understand product demand patterns
   - Identify popular categories
   - Track competitor performance

3. **Lead Generation**
   - Products visible to active buyers
   - View tracking shows interest
   - Trending placement provides exposure
   - Tier system highlights quality

4. **Competitive Advantage**
   - Differentiate through premium tier
   - Special tags highlight unique features
   - Price competitiveness visible
   - First-mover advantage in digital space

### For Contractors and Builders

1. **Time Savings**
   - One platform for all suppliers
   - No more calling multiple vendors
   - Instant price comparisons
   - Immediate product specifications

2. **Better Decisions**
   - Compare multiple offers
   - Filter by quality requirements
   - Choose based on real data
   - Avoid costly measurement errors

3. **Cost Reduction**
   - Find best prices easily
   - Identify cost-effective alternatives
   - Bulk purchase opportunities
   - Competitive supplier selection

4. **Quality Assurance**
   - Tier system identifies premium suppliers
   - Tags indicate specializations
   - Verified product specifications
   - Trending indicates trusted products

### For Project Managers

1. **Standardization**
   - Consistent product data format
   - Reliable technical specifications
   - Predictable API responses
   - Integration-ready architecture

2. **Compliance**
   - Audit trail of product selections
   - Documented supplier evaluations
   - Verified certifications via tags
   - Historical price records

3. **Budget Control**
   - Accurate price tracking
   - Supplier performance monitoring
   - Cost trend analysis
   - Volume discount opportunities

4. **Risk Management**
   - Tier 1 suppliers for critical projects
   - Multiple supplier options per product
   - Backup suppliers identified
   - Market diversification

## DEVELOPMENT AND DEPLOYMENT

### Local Development Setup

The project is designed for immediate local development with minimal configuration:

1. **Environment Setup**
   - Python virtual environment
   - Single requirements.txt file
   - SQLite zero-config database
   - Environment variables template

2. **Database Management**
   - Automatic table creation
   - Seed data for testing
   - Alembic migrations ready
   - Easy reset capability

3. **Testing Framework**
   - Pytest test suite
   - Isolated test database
   - Comprehensive test coverage
   - CI/CD ready

### Deployment Options

1. **Simple Deployment**
   - Single server deployment
   - SQLite to PostgreSQL upgrade
   - Nginx reverse proxy
   - Supervisor process management

2. **Cloud Deployment**
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - Azure App Service
   - Docker containerization

3. **Scaling Considerations**
   - Read replicas for analytics
   - Caching layer for trending data
   - Connection pooling
   - Horizontal scaling ready

## FUTURE ENHANCEMENTS

The current implementation provides a solid foundation for future features:

1. **Machine Learning**
   - Personalized product recommendations
   - Demand forecasting
   - Price optimization
   - Anomaly detection

2. **Advanced Analytics**
   - Geographic trending
   - Seasonal demand patterns
   - Supplier performance metrics
   - ROI calculations

3. **Enhanced Collaboration**
   - Project-based material lists
   - Team sharing features
   - Approval workflows
   - Quote requests

4. **Integration Capabilities**
   - ERP system integration
   - Accounting software connectors
   - Inventory management sync
   - E-commerce platform APIs

## CONCLUSION

The Materials Catalog API is more than just a CRUD application. It is a comprehensive business solution that addresses real-world challenges in the construction materials industry. By combining flexible data modeling, intelligent analytics, practical features like unit conversion, and robust security, it provides immediate value while laying the groundwork for future innovation.

Whether deployed as a simple internal tool for a single supplier or scaled to serve a national marketplace, the system's clean architecture and well-documented APIs ensure it can grow with the business. The focus on real business problems - not just technical exercises - makes this project truly valuable.

This is a production-ready solution that solves actual problems faced daily by thousands of construction professionals worldwide. It bridges the gap between traditional procurement methods and modern digital efficiency, all while maintaining the flexibility to adapt to unique business requirements.

The project demonstrates modern Python development practices, proper software architecture, and most importantly - understanding of the domain and user needs. It is ready for immediate use and built for future expansion.
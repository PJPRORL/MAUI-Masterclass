# MAUI Element Catalog

This catalog lists common .NET MAUI elements and their frequently used attributes. Use this as a reference when building your UI.

## 📐 Common Layout Properties
These properties apply to almost all visual elements (Layouts and Controls).

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `Margin` | `Thickness` | Space *outside* the element. | `Margin="10"` or `Margin="10,5,10,5"` |
| `Padding` | `Thickness` | Space *inside* the element (mostly for Layouts). | `Padding="20"` |
| `BackgroundColor` | `Color` | Background color of the element. | `BackgroundColor="LightGray"` |
| `WidthRequest` | `Double` | Desired width. | `WidthRequest="100"` |
| `HeightRequest` | `Double` | Desired height. | `HeightRequest="50"` |
| `HorizontalOptions` | `LayoutOptions` | Alignment horizontally. | `Start`, `Center`, `End`, `Fill` |
| `VerticalOptions` | `LayoutOptions` | Alignment vertically. | `Start`, `Center`, `End`, `Fill` |
| `IsVisible` | `Boolean` | Shows or hides the element. | `IsVisible="True"` |
| `Opacity` | `Double` | Transparency (0.0 to 1.0). | `Opacity="0.5"` |

---

## 📦 Layouts

### VerticalStackLayout / HorizontalStackLayout
Organizes children sequentially.

| Property | Type | Description |
|----------|------|-------------|
| `Spacing` | `Double` | Space between children. |

### Grid
Organizes children in rows and columns.

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `RowDefinitions` | `String` | Height of rows. | `RowDefinitions="Auto, *, 100"` |
| `ColumnDefinitions` | `String` | Width of columns. | `ColumnDefinitions="*, 2*"` |
| `RowSpacing` | `Double` | Space between rows. | `RowSpacing="10"` |
| `ColumnSpacing` | `Double` | Space between columns. | `ColumnSpacing="10"` |

**Attached Properties (on children):**
- `Grid.Row="0"`
- `Grid.Column="1"`
- `Grid.RowSpan="2"`
- `Grid.ColumnSpan="2"`

---

## 🎮 Controls

### Label
Displays text.

| Property | Type | Description |
|----------|------|-------------|
| `Text` | `String` | The text to display. |
| `TextColor` | `Color` | Color of the text. |
| `FontSize` | `Double` | Size of the text. |
| `FontAttributes` | `FontAttributes` | `Bold`, `Italic`, `None`. |
| `HorizontalTextAlignment` | `TextAlignment` | `Start`, `Center`, `End`. |
| `VerticalTextAlignment` | `TextAlignment` | `Start`, `Center`, `End`. |
| `LineBreakMode` | `LineBreakMode` | `NoWrap`, `WordWrap`, `TailTruncation`. |

### Button
Clickable button.

| Property | Type | Description |
|----------|------|-------------|
| `Text` | `String` | Button label. |
| `Command` | `ICommand` | Bindable command to execute on click. |
| `CommandParameter` | `Object` | Parameter to pass to the command. |
| `Clicked` | `Event` | Event handler for click (Code-behind). |
| `CornerRadius` | `Int` | Roundness of corners. |
| `BorderColor` | `Color` | Color of the border. |
| `BorderWidth` | `Double` | Width of the border. |
| `ImageSource` | `ImageSource` | Icon to display on the button. |

### Entry
Single-line text input.

| Property | Type | Description |
|----------|------|-------------|
| `Text` | `String` | The input text (Two-way binding). |
| `Placeholder` | `String` | Hint text when empty. |
| `PlaceholderColor` | `Color` | Color of placeholder text. |
| `IsPassword` | `Boolean` | Hides text (for passwords). |
| `Keyboard` | `Keyboard` | `Text`, `Numeric`, `Email`, `Telephone`. |
| `IsReadOnly` | `Boolean` | Prevents editing. |
| `MaxLength` | `Int` | Max characters allowed. |
| `ReturnType` | `ReturnType` | `Done`, `Next`, `Search`, `Send`. |

### Image
Displays an image.

| Property | Type | Description |
|----------|------|-------------|
| `Source` | `ImageSource` | URL or filename of the image. |
| `Aspect` | `Aspect` | `AspectFit`, `AspectFill`, `Fill`. |

---

## 📚 Data Views

### CollectionView
Displays a list of items.

| Property | Type | Description |
|----------|------|-------------|
| `ItemsSource` | `IEnumerable` | List of data to display. |
| `SelectionMode` | `SelectionMode` | `None`, `Single`, `Multiple`. |
| `EmptyView` | `Object` | Content to show when list is empty. |
| `Header` | `Object` | Content at the top of the list. |
| `Footer` | `Object` | Content at the bottom of the list. |

**ItemTemplate:**
Defines how each item looks.
```xml
<CollectionView.ItemTemplate>
    <DataTemplate>
        <StackLayout>
            <Label Text="{Binding Name}" />
        </StackLayout>
    </DataTemplate>
</CollectionView.ItemTemplate>
```

# Hoofdstuk 3 – Interactie: BaseViewModel, RelayCommand & CollectionView

Nu draait alles nog vrij statisch. We voegen nu:
- Een `BaseViewModel` voor gedeelde state.
- `RelayCommand` voor acties vanuit de UI.
- Geavanceerde dingen in `CollectionView` (EmptyView, RefreshView, Swipe-acties, selectie).

## 3.1 BaseViewModel: gedeelde logica centraliseren

Veel ViewModels hebben `IsBusy`, `Title`, `IsNotBusy`. We willen die niet telkens opnieuw schrijven.

**ViewModels/BaseViewModel.cs**
```csharp
using CommunityToolkit.Mvvm.ComponentModel;

namespace MijnMauiApp.ViewModels;

public partial class BaseViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(IsNotBusy))]
    private bool isBusy;

    [ObservableProperty]
    private string title;

    public bool IsNotBusy => !IsBusy;
}
```
Nu kunnen alle ViewModels hiervan erven:
```csharp
public partial class TodoViewModel : BaseViewModel { ... }
```

## 3.2 RelayCommand: acties zonder code-behind events

In plaats van in XAML `Clicked="Button_Clicked"` te gebruiken, schrijven we methodes in de ViewModel en markeren die met `[RelayCommand]`.

**Voorbeeld: taak toevoegen**

```csharp
public partial class TodoViewModel : BaseViewModel
{
    // ... properties ...

    [RelayCommand]
    async Task VoegTaakToeAsync()
    {
        if (string.IsNullOrWhiteSpace(HuidigeTitel)) return;

        IsBusy = true;
        try
        {
            var nieuweTaak = new TodoItem
            {
                Titel = HuidigeTitel,
                IsAfgerond = false
            };
            await _repository.VoegTaakToeAsync(nieuweTaak);
            Taken.Add(nieuweTaak);
            HuidigeTitel = string.Empty;
        }
        finally
        {
            IsBusy = false;
        }
    }
}
```

**In XAML koppelen**
```xml
<Button Text="Toevoegen"
        Command="{Binding VoegTaakToeCommand}"
        IsEnabled="{Binding IsNotBusy}" />
```
Methode naam in C#: `VoegTaakToeAsync`. Command in XAML: `VoegTaakToeCommand` (toolkit verwijdert Async en plakt Command eraan).

## 3.3 Commands met parameters: items verwijderen

Je wilt bijvoorbeeld via een swipe of een knop naast elk item een taak verwijderen.

**ViewModel: command met parameter**
```csharp
[RelayCommand]
async Task VerwijderTaakAsync(TodoItem taakOmTeVerwijderen)
{
    if (taakOmTeVerwijderen == null) return;
    Taken.Remove(taakOmTeVerwijderen);
    await _repository.VerwijderTaakAsync(taakOmTeVerwijderen);
}
```

**XAML: binnen CollectionView.ItemTemplate + SwipeView**
```xml
<CollectionView.ItemTemplate>
    <DataTemplate x:DataType="models:TodoItem">
        <SwipeView>
            <SwipeView.RightItems>
                <SwipeItems>
                    <SwipeItem Text="Verwijder"
                               BackgroundColor="Red"
                               Command="{Binding Source={RelativeSource AncestorType={x:Type vm:TodoViewModel}}, Path=VerwijderTaakCommand}"
                               CommandParameter="{Binding .}" />
                </SwipeItems>
            </SwipeView.RightItems>
            <HorizontalStackLayout Padding="10" Spacing="10">
                <Label Text="{Binding Titel}" />
            </HorizontalStackLayout>
        </SwipeView>
    </DataTemplate>
</CollectionView.ItemTemplate>
```

## 3.4 Geavanceerde CollectionView features

**A. EmptyView: lege lijst mooi tonen**
```xml
<CollectionView ItemsSource="{Binding Taken}">
    <CollectionView.EmptyView>
        <VerticalStackLayout VerticalOptions="Center" HorizontalOptions="Center">
            <Label Text="Geen taken gevonden!" FontAttributes="Bold" />
            <Label Text="Voeg snel een eerste taak toe." TextColor="Gray" />
        </VerticalStackLayout>
    </CollectionView.EmptyView>
</CollectionView>
```

**B. Pull-to-Refresh via RefreshView**
```xml
<RefreshView IsRefreshing="{Binding IsBusy}"
             Command="{Binding LaadDataCommand}">
    <CollectionView ItemsSource="{Binding Taken}">
        <!-- ... -->
    </CollectionView>
</RefreshView>
```

**C. Selectie (optionele navigatie naar detail)**
```xml
<CollectionView ItemsSource="{Binding Taken}"
                SelectionMode="Single"
                SelectionChangedCommand="{Binding GaNaarDetailsCommand}"
                SelectionChangedCommandParameter="{Binding SelectedItem, Source={RelativeSource Self}}">
```

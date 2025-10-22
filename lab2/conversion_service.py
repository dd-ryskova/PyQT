from currency_signals import RUBSignals, USDSignals, EURSignals

class ConversionService:
    def __init__(self):
        self.usd_signals = USDSignals()
        self.eur_signals = EURSignals()
        self.rub_signals = RUBSignals()
        
        self.setup_exchange_rates()
        
    def setup_exchange_rates(self):
        self.usd_to_eur = 0.862069
        self.usd_to_rub = 81.270000
        self.eur_to_usd = 1.160000
        self.eur_to_rub = 93.900000
        self.rub_to_usd = 0.012305
        self.rub_to_eur = 0.010650
    
    def convert_from_usd(self, value, eur_input, rub_input):
        try:
            if value:
                usd_amount = float(value)
                self.usd_signals.usdConversionStarted.emit()
                
                eur_input.update_value(str(round(usd_amount * self.usd_to_eur, 2)))
                rub_input.update_value(str(round(usd_amount * self.usd_to_rub, 2)))
                
                results = {
                    'EUR': round(usd_amount * self.usd_to_eur, 2),
                    'RUB': round(usd_amount * self.usd_to_rub, 2)
                }
                self.usd_signals.usdConversionCompleted.emit({
                    'amount': usd_amount, 
                    'results': results
                })
        except ValueError:
            pass
    
    def convert_from_eur(self, value, usd_input, rub_input):
        try:
            if value:
                eur_amount = float(value)
                self.eur_signals.eurConversionStarted.emit()
                
                usd_input.update_value(str(round(eur_amount * self.eur_to_usd, 2)))
                rub_input.update_value(str(round(eur_amount * self.eur_to_rub, 2)))
                
                results = {
                    'USD': round(eur_amount * self.eur_to_usd, 2),
                    'RUB': round(eur_amount * self.eur_to_rub, 2)
                }
                self.eur_signals.eurConversionCompleted.emit({
                    'amount': eur_amount, 
                    'results': results
                })
        except ValueError:
            pass
    
    def convert_from_rub(self, value, usd_input, eur_input):
        try:
            if value:
                rub_amount = float(value)
                self.rub_signals.rubConversionStarted.emit()
                
                usd_input.update_value(str(round(rub_amount * self.rub_to_usd, 2)))
                eur_input.update_value(str(round(rub_amount * self.rub_to_eur, 2)))
                
                results = {
                    'USD': round(rub_amount * self.rub_to_usd, 2),
                    'EUR': round(rub_amount * self.rub_to_eur, 2)
                }
                self.rub_signals.rubConversionCompleted.emit({
                    'amount': rub_amount, 
                    'results': results
                })
        except ValueError:
            pass
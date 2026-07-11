import { Container, Typography } from '@mui/material';

export function NotFoundPage() {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography component="h1" variant="h4">
        Страница не найдена
      </Typography>
    </Container>
  );
}
